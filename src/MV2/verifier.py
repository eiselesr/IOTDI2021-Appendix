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

    def process(self, input, context=None):
        pass

    def result_listener(self, consumer, msg):
        data = {'result': msg.value(),
                'supplier': msg.properties()['supplier'],
                'allocationid': msg.properties()['allocationid'],
                'msg-num': msg.properties()['msg-num']}
        self.df_results = self.df_results.append(data, ignore_index=True)
        consumer.acknowledge(msg)
        self.check()

    def check(self):
        need_checks = self.df_allocations[(self.df_allocations['end'] > time.time())]
        expired_allocations = need_checks['allocationid'].values.tolist()
        for a in expired_allocations:
            result = "ok"
            messages = self.df_results[self.df_results['allocationid']==a]
            for message_number in messages['msg-num'].unique():
                if len(messages[messages['msg-num']==message_number]['result'].unique()) > 1:
                    result = "fail"
            producer = self.client.create_producer(f"persistent://{customer.user}/{service_name}/check-{a}")

    def allocation_listener(self, consumer, msg):
        consumer.acknowledge(msg)
        data = {"allocationid": msg.value().allocationid,
                "customer": msg.value().customer,
                "suppliers": msg.value().suppliers,
                "start": msg.value().start,
                "end": msg.value().end,
                "service_name": msg.value().service_name,
                "price": msg.value().price,
                "replicas": msg.value().replicas}
        self.df_allocations = self.df_allocations.append(data, ignore_index=True)
        for supplier in msg.value().suppliers:
            PulsarREST.create_namespace(pulsar_admin_url=cfg.pulsar_admin_url, tenant=supplier, namespace=msg.value().service_name)
            self.client.subscribe(topic="persistent://{}/{}/{}".format(supplier, msg.value().service_name, msg.value().jobid),
                                  subscription_name="verifier-{}-{}-{}".format(self.tenant, msg.value().jobid, supplier),
                                  initial_position=pulsar.InitialPosition.Earliest,
                                  consumer_type=pulsar.ConsumerType.Exclusive,
                                  message_listener=self.result_listener)


