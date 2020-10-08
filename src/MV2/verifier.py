import re
import pulsar
import pandas as pd
import time
from . import cfg, schema, PulsarREST


class Verifier:
    def __init__(self, tenant):
        self.df_results = pd.DataFrame(columns=['result',
                                                'supplier'
                                                'jobid'])

        self.df_allocations = pd.DataFrame(columns=['jobid',
                                                    'customer',
                                                    'suppliers',
                                                    'replicas',
                                                    'num_messages',
                                                    'service_name'])
        self.tenant = tenant
        self.client = pulsar.Client(cfg.pulsar_url)
        self.logger = self.client.create_producer(topic=f"{cfg.tenant}/{cfg.namespace}/{cfg.logger_topic}")

        allocation_topic = f"persistent://{cfg.tenant}/{cfg.namespace}/allocation_topic"
        self.allocation_consumer = self.client.subscribe(allocation_topic,
                                                         schema=pulsar.schema.JsonSchema(schema.AllocationSchema),
                                                         subscription_name="allocation{}".format(tenant),
                                                         initial_position=pulsar.InitialPosition.Earliest,
                                                         consumer_type=pulsar.ConsumerType.Exclusive,
                                                         message_listener=self.allocation_listener)
        self.logger.send(f"verifier: done initializing verifier".encode("utf-8"))

    def process(self, input, context=None):
        pass

    def result_listener(self, consumer, msg):
        self.logger.send(f"verifier: got message on topic {msg.topic_name()}".encode("utf-8"))
        val = int(msg.data().decode("utf-8"))
        jobid = msg.properties()['jobid']
        supplier = msg.properties()['supplier']
        self.df_results = self.df_results.append({'result': val, 'supplier': supplier, 'jobid': jobid}, ignore_index=True)
        consumer.acknowledge(msg)

        # check if this completes job
        print(jobid)
        job = self.df_allocations[self.df_allocations['jobid']==str(jobid)].iloc[0]
        print(job)
        complete = True
        tester = []
        for s in job['suppliers']:
            temp = self.df_results.loc[((self.df_results['supplier']==s) & (self.df_results['jobid']==jobid)), 'result'].values.tolist()
            if len(temp) == job['replicas']:
                tester.append(temp)
            else:
                complete = False
        if complete:
            correct = True
            for i in range(1, len(tester)):
                if tester[0] != tester[i]:
                    correct = False
                    break
            p = self.client.create_producer(topic=f"persistent://{job['customer']}/{job['service_name']}/{jobid}-output")
            if correct:
                for val in tester[0]:
                    p.send(str(val).encode("utf-8"))
            else:
                p.send("job failed".encode("utf-8"))
            p.close()

    def allocation_listener(self, consumer, msg):
        time.sleep(3)
        consumer.acknowledge(msg)
        self.df_allocations = self.df_allocations.append({'jobid': msg.value().jobid,
                                    'customer': msg.value().customer,
                                    'suppliers': msg.value().suppliers,
                                    'num_messages': msg.value().num_messages,
                                    'service_name': msg.value().service_name,
                                    'replicas': msg.value().replicas}, ignore_index=True)
        print(self.df_allocations.head())
        for supplier in msg.value().suppliers:
            PulsarREST.create_namespace(pulsar_admin_url=cfg.pulsar_admin_url, tenant=supplier, namespace=msg.value().service_name)
            topic = "persistent://{}/{}/{}".format(supplier, msg.value().service_name, msg.value().jobid)
            self.client.subscribe(topic,
                                  subscription_name="verifier-{}-{}-{}".format(self.tenant, msg.value().jobid, supplier),
                                  initial_position=pulsar.InitialPosition.Earliest,
                                  consumer_type=pulsar.ConsumerType.Exclusive,
                                  message_listener=self.result_listener)
            self.logger.send(f"verifier: started listening to topic {topic}".encode("utf-8"))


