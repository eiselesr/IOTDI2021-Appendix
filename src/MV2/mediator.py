import pulsar
import pandas as pd
import time
import threading
from copy import deepcopy
from . import cfg, schema, PulsarREST, queries


class Mediator:
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
                                                    'timestamp',
                                                    'supplierbehaviors'])

        # pulsar client
        self.client = pulsar.Client(cfg.pulsar_url)

        # producer - logger
        self.logger = self.client.create_producer(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/{cfg.logger_topic}")
        self.logger.send(f"mediator: initializing".encode("utf-8"))

        # consumer - allocation topic
        self.allocation_consumer = self.client.subscribe(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/allocation_topic",
                                                         schema=pulsar.schema.JsonSchema(schema.AllocationSchema),
                                                         subscription_name=f"{self.user}-allocation-subscription",
                                                         initial_position=pulsar.InitialPosition.Latest,
                                                         consumer_type=pulsar.ConsumerType.Exclusive,
                                                         message_listener=self.allocation_listener)

        while True:
            time.sleep(0.1)

    def allocation_listener(self, consumer, msg):
        self.logger.send(f"mediator: got an allocation {msg.value().allocationid}".encode("utf-8"))

        # add allocation to df_allocations
        data = {"jobid": msg.value().jobid,
                "allocationid": msg.value().allocationid,
                "customer": msg.value().customer,
                "suppliers": msg.value().suppliers,
                "start": msg.value().start,
                "end": msg.value().end,
                "service_name": msg.value().service_name,
                "price": msg.value().price,
                "replicas": msg.value().replicas,
                "timestamp": msg.value().timestamp,
                "supplierbehaviors": msg.value().supplierbehaviors}
        #self.df_allocations = self.df_allocations.append(data, ignore_index=True)

        # start a consumer if customer-service_name not already seen
        tf = len(self.df_allocations[(self.df_allocations['customer']==data['customer']) & (self.df_allocations['service_name']==data['service_name'])])
        self.logger.send(f"mediator-{self.user}: current length of customer {tf}".encode("utf-8"))
        if tf == 0:
            consumer = self.client.subscribe(topic=f"persistent://{data['customer']}/{data['service_name']}/check",
                                             schema=pulsar.schema.JsonSchema(schema.CheckSchema),
                                             subscription_name=f"{self.user}-{data['customer']}-{data['service_name']}-{data['allocationid']}",
                                             initial_position=pulsar.InitialPosition.Earliest,
                                             consumer_type=pulsar.ConsumerType.Exclusive,
                                             message_listener=self.check_listener)
            self.logger.send(f"mediator-{self.user}: started consumer".encode("utf-8"))

        # add allocation to df_allocations
        self.df_allocations = self.df_allocations.append(data, ignore_index=True)
        consumer.acknowledge(msg)

    def check_listener(self, consumer, msg):
        self.logger.send(f"mediator-{self.user}: got a check message".encode("utf-8"))
        supplierspass, suppliersfail = [], []
        for i in range(len(msg.value().suppliers)):
            if msg.value().supplierbehaviors[i] == "correct":
                supplierspass.append(msg.value().suppliers[i])
            else:
                suppliersfail.append(msg.value().suppliers[i])
        if len(supplierspass) == 0:
            supplierspass.append("none")
        if len(suppliersfail) == 0:
            suppliersfail.append("none")
        data = schema.MediationSchema(
            result=msg.value().result,
            customer=msg.value().customer,
            supplierspass=supplierspass,
            suppliersfail=suppliersfail,
            service_name=msg.value().service_name,
            jobid=msg.value().jobid,
            allocationid=msg.value().allocationid,
            checktimestamp=msg.value().timestamp,
            mediationtimestamp=time.time()
        )
        # write to mediation topic
        producer = self.client.create_producer(topic="persistent://{}/{}/mediation".format(msg.value().customer, msg.value().service_name),
                                               schema=pulsar.schema.JsonSchema(schema.MediationSchema))
        producer.send(data)
        producer.close()
        self.logger.send(f"mediator-{self.user}: send to mediation topic".encode("utf-8"))
        consumer.acknowledge(msg)
