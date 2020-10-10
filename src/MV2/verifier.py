import re
import pulsar
import pandas as pd
import time
from . import cfg, schema, PulsarREST


class Verifier:
    def __init__(self, tenant):
        self.df_results = pd.DataFrame(columns=['result',
                                                'supplier'
                                                'allocationid',
                                                'msg-num'])

        self.df_allocations = pd.DataFrame(columns=['allocationid',
                                                    'customer',
                                                    'suppliers',
                                                    'start',
                                                    'end',
                                                    'service_name',
                                                    'price',
                                                    'replicas'])
        self.tenant = tenant

        # pulsar client
        self.client = pulsar.Client(cfg.pulsar_url)

        # producer - logger
        self.logger = self.client.create_producer(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/{cfg.logger_topic}")
        self.logger.send(f"verifier: initializing".encode("utf-8"))

        # consumer - allocation topic
        self.allocation_consumer = self.client.subscribe(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/allocation_topic",
                                                         schema=pulsar.schema.JsonSchema(schema.AllocationSchema),
                                                         subscription_name="allocation{}".format(tenant),
                                                         initial_position=pulsar.InitialPosition.Earliest,
                                                         consumer_type=pulsar.ConsumerType.Exclusive,
                                                         message_listener=self.allocation_listener)

        time.sleep(10)
        while True:
            expire_time = time.time() + cfg.window
            expired_allocations = self.df_allocations[(self.df_allocations['end'] > expire_time)]
            if len(expired_allocations) > 0:
                print(expired_allocations.head())
                remove = []
                for k, v in expired_allocations.iterrows():
                    remove.append(k)
                    self.process(v)
                self.df_allocations = self.df_allocations[~self.df_allocations['allocationid'].isin(remove)]
                self.df_results = self.df_results[~self.df_results['allocationid'].isin(remove)]
            time.sleep(10)

    def stream_listener(self, consumer, msg):
        data = {'result': msg.value(),
                'supplier': msg.properties()['supplier'],
                'allocationid': msg.properties()['allocationid'],
                'msg-num': msg.properties()['msg-num']}
        self.df_results = self.df_results.append(data, ignore_index=True)
        consumer.acknowledge(msg)

    def allocation_listener(self, consumer, msg):
        self.logger.send(f"verifier: got an allocation {msg.value().allocationid}".encode("utf-8"))
        # add allocation to df_allocations
        data = {"allocationid": msg.value().allocationid,
                "customer": msg.value().customer,
                "suppliers": msg.value().suppliers,
                "start": msg.value().start,
                "end": msg.value().end,
                "service_name": msg.value().service_name,
                "price": msg.value().price,
                "replicas": msg.value().replicas}
        self.df_allocations = self.df_allocations.append(data, ignore_index=True)

        # for each supplier in allocation, create a listener for supplier's results
        for supplier in msg.value().suppliers:
            PulsarREST.create_namespace(pulsar_admin_url=cfg.pulsar_admin_url, tenant=supplier, namespace=msg.value().service_name)
            self.client.subscribe(topic=f"persistent://{supplier}/{msg.value().service_name}/output-{msg.value().allocationid}",
                                  subscription_name=f"verifier-{self.tenant}-{msg.value().allocationid}-{supplier}",
                                  initial_position=pulsar.InitialPosition.Earliest,
                                  consumer_type=pulsar.ConsumerType.Exclusive,
                                  message_listener=self.stream_listener)
        consumer.acknowledge(msg)

    def process(self, allocation):
        self.logger.send(f"verifier: starting verification of {allocation['allocationid']}".encode("utf-8"))
        result_producer = self.client.create_producer(topic=f"persistent://{allocation['customer']}/{allocation['service_name']}/output")
        allocation_results = self.df_results[self.df_results['allocationid']==allocation['allocationid']]
        result = "pass"
        for msg_num in allocation_results['msg-num'].unique():
            temp = allocation_results.loc[(allocation_results['msg-num']==msg_num), 'result']
            if len(temp.unique()) != 1:
                check_status = "fail"
                result = "fail"
                val = "none".encode("utf-8")
            else:
                check_status = "pass"
                val = str(temp['result'][0]).encode("utf-8")
            result_producer.send(val, properties={"check-status": check_status, "msg-num": str(msg_num)})
        check_producer = self.client.create_producer(topic=f"persistent://{allocation['customer']}/{allocation['service_name']}/check-{allocation['allocationid']}",
                                                     schema=pulsar.schema.JsonSchema(schema.CheckSchema))
        check = schema.CheckSchema(
            result=result,
            status="done",
            startmessage=int(allocation_results['msg-num'].min()),
            endmessage=int(allocation_results['msg-num'].max()),
            allocationid=allocation['allocationid'])
        check_producer.send(check)
        result_producer.close()
        check_producer.close()
        self.logger.send(f"verifier: verified allocation {allocation['allocationid']}, result={result}".encode("utf-8"))


