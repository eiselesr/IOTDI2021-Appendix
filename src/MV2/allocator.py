import re
import uuid
import datetime
import pulsar
import time
from . import PulsarREST, cfg, schema


# class Fulfillment(pulsar.Function):
class Allocator:
    def __init__(self):
        self.id = self.register()
        self.customer_offers = []
        self.supplier_offers = []

        # pulsar client
        self.client = pulsar.Client(cfg.pulsar_url)

        # producer - logger
        self.logger = self.client.create_producer(topic=f"{cfg.tenant}/{cfg.namespace}/{cfg.logger_topic}")
        self.logger.send(f"allocator: initializing".encode("utf-8"))

        # producer - allocation
        self.allocation_producer = self.client.create_producer(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/allocation_topic",
                                                               schema=pulsar.schema.JsonSchema(schema.AllocationSchema))

        # consumer - supply and customer offers
        self.offer_consumer = self.client.subscribe(topic=re.compile(f"persistent://{cfg.tenant}/{cfg.namespace}/.*_offers"),
                                                    schema=pulsar.schema.JsonSchema(schema.OfferSchema),
                                                    subscription_name="offer-sub-2",
                                                    initial_position=pulsar.InitialPosition.Latest,
                                                    message_listener=self.offer_listener)
        while True:
            time.sleep(0.1)

    def offer_listener(self, consumer, msg):
        consumer.acknowledge(msg)
        self.logger.send(f"allocator: got a an offer with topic_name {msg.topic_name()}".encode("utf-8"))

        # see if customer or supply offers, then append to corresponding stack
        if "customer" in msg.topic_name():
            self.customer_offers.append(msg.value())
        if "supply" in msg.topic_name():
            self.supplier_offers.append(msg.value())

        # see if there is a match
        if len(self.customer_offers) > 0:
            num_replicas_needed = self.customer_offers[0].replicas
            if len(self.supplier_offers) >= num_replicas_needed:
                customer = self.customer_offers.pop(0)
                suppliers = []
                for i in range(customer.replicas):
                    supplier = self.supplier_offers.pop(0)
                    suppliers.append(supplier.user)
                allocation = schema.AllocationSchema(
                    jobid=customer.jobid,
                    allocationid=customer.allocationid,
                    customer=customer.user,
                    suppliers=suppliers,
                    start=customer.start,
                    end=customer.end,
                    service_name=customer.service_name,
                    price=customer.price,
                    replicas=customer.replicas,
                    timestamp=time.time())
                self.allocation_producer.send(allocation)
                self.logger.send(f"allocator: allocated job {customer.allocationid}, customer {customer.user} and suppliers {suppliers}".encode("utf-8"))

    def register(self):
        # blockchain shenanigans
        return 0




