import pulsar
import pandas as pd
import time
import threading
from copy import deepcopy
from . import cfg, schema, PulsarREST, queries


class Verifier:
    def __init__(self, user):
        self.user = user
        self.df_allocations = pd.DataFrame(columns=['jobid',
                                                    'allocationid',
                                                    'customer',
                                                    'suppliers',
                                                    'start',
                                                    'end',
                                                    'service_name',
                                                    'price',
                                                    'replicas',
                                                    'timestamp'])

        # pulsar client
        self.client = pulsar.Client(cfg.pulsar_url)

        # producer - logger
        self.logger = self.client.create_producer(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/{cfg.logger_topic}")
        self.logger.send(f"verifier: initializing".encode("utf-8"))

        # consumer - allocation topic
        self.allocation_consumer = self.client.subscribe(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/allocation_topic",
                                                         schema=pulsar.schema.JsonSchema(schema.AllocationSchema),
                                                         subscription_name=f"{self.user}-allocation-subscription",
                                                         initial_position=pulsar.InitialPosition.Latest,
                                                         consumer_type=pulsar.ConsumerType.Exclusive,
                                                         message_listener=self.allocation_listener)

        # periodically check for expired allocations
        while True:
            time.sleep(0.1)
            #t = threading.Thread(target=self.flush_allocations)
            #t.start()
            #t.join()

    def allocation_listener(self, consumer, msg):
        consumer.acknowledge(msg)
        self.logger.send(f"verifier: got an allocation {msg.value().allocationid}".encode("utf-8"))
        data = {"jobid": msg.value().jobid,
                "allocationid": msg.value().allocationid,
                "customer": msg.value().customer,
                "suppliers": msg.value().suppliers,
                "start": msg.value().start,
                "end": msg.value().end,
                "service_name": msg.value().service_name,
                "price": msg.value().price,
                "replicas": msg.value().replicas,
                "timestamp": msg.value().timestamp}
        self.df_allocations = self.df_allocations.append(data, ignore_index=True)
        self.flush_allocations()

    def flush_allocations(self):
        df = deepcopy(self.df_allocations)
        expired_allocations = df.loc[df['end'] < time.time()+3]
        if len(expired_allocations) > 0:
            for k, allocation in expired_allocations.iterrows():
                self.verify(allocation)
            expired_allocationids = expired_allocations['allocationid'].tolist()
            self.df_allocations = self.df_allocations[~self.df_allocations['allocationid'].isin(expired_allocationids)]
            self.logger.send(f"verifier: verified allocations {expired_allocationids}".encode("utf-8"))

    def verify(self, allocation):
        query = "SELECT * FROM output WHERE allocationid = '{}'".format(allocation['allocationid'])
        df = queries.presto_query(query,
                                  user='verifier',
                                  schema="{}/{}".format(allocation['customer'], allocation['service_name']))
        result = 'pass'
        for msgnum in df['msgnum'].unique():
            temp = df.loc[df['msgnum']==msgnum, 'value']
            if len(temp.unique()) != 1:
                result = "fail"
                break

        # write to check topic
        producer = self.client.create_producer(topic="persistent://{}/{}/check".format(allocation['customer'], allocation['service_name']),
                                               schema=pulsar.schema.JsonSchema(schema.CheckSchema))
        data = schema.CheckSchema(
            result = result,
            customer=allocation['customer'],
            suppliers=allocation['suppliers'],
            service_name=allocation['service_name'],
            jobid=allocation['jobid'],
            allocationid=allocation['allocationid'],
            timestamp=time.time()
        )
        producer.send(data)
        producer.close()

