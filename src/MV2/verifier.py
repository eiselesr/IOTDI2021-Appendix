import re
import pulsar
import pandas as pd
import time
import threading
from . import cfg, schema, PulsarREST

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
                                                         initial_position=pulsar.InitialPosition.Earliest,
                                                         consumer_type=pulsar.ConsumerType.Exclusive,
                                                         message_listener=self.allocation_listener)

        flush_time = time.time() + 10
        while True:
            if time.time() >= flush_time:
                t = threading.Thread(target=thread_function)
                t.start()
                t.join()
                flush_time = time.time() + 10


    def allocation_listener(self, consumer, msg):
        self.logger.send(f"verifier: got an allocation {msg.value().allocationid}".encode("utf-8"))
        data = {"jobid": msg.value().jobid,
                "allocationid": msg.value().allocationid,
                "customer": msg.value().customer,
                "suppliers": msg.value().suppliers,
                "start": msg.value().start,
                "end": msg.value().end,
                "service_name": msg.value().service_name,
                "price": msg.value().price,
                "replicas": msg.values().replicas,
                "timestamp": msg.value().timestamp}
        self.df_allocations = self.df_allocations.append(data, ignore_index=True)
        consumer.acknowledge(msg)