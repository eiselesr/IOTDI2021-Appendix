import re
import uuid
import datetime
import pulsar
from . import PulsarREST, cfg, schema


# class Fulfillment(pulsar.Function):
class Allocator:
    def __init__(self):
        self.id = self.register()
        self.customer_offers = []
        self.supplier_offers = []

        client = pulsar.Client(cfg.pulsar_url)

        self.consumer = client.subscribe(re.compile(f"persistent://{cfg.tenant}/{cfg.namespace}/.*_offers"),
                                         schema=pulsar.schema.JsonSchema(schema.OfferSchema),
                                         subscription_name="offer-sub",
                                         initial_position=pulsar.InitialPosition.Latest,
                                         message_listener=self.listener)

        self.producer = client.create_producer(topic="allocation_topic",
                                               schema=pulsar.schema.JsonSchema(schema.AllocationSchema))

        self.logger = self.client.create_producer(topic=f"{cfg.tenant}/{cfg.namespace}/{cfg.logger_topic}")
        self.logger.send(f"allocator-{self.tenant}: done initializing allocator".encode("utf-8"))

    def listener(self, consumer, msg):
        now = datetime.datetime.now(tz=datetime.timezone.utc)

        if "customer" in msg.topic_name():
            self.customer_offers.append(msg.value())

        if "supply" in msg.topic_name():
            self.supplier_offers.append(msg.value())

        if len(self.customer_offers) > 0:
            num_replicas_needed = self.customer_offers[0].replicas
            if len(self.supplier_offers) >= num_replicas_needed:
                customer = self.customer_offers.pop()
                suppliers = []
                for i in range(customer.replicas):
                    supplier = self.supplier_offers.pop()
                    suppliers.append(supplier.user)
                allocation = schema.AllocationSchema(
                    jobid=customer.jobid,
                    customer=customer.user,
                    suppliers=suppliers,
                    start=customer.start,
                    end=customer.end,
                    service_name=customer.service_name,
                    price=customer.price,
                    replicas=customer.replicas,
                    num_messages=customer.num_messages)
                self.producer.send(allocation, event_timestamp=int(datetime.datetime.timestamp(now)))
        consumer.acknowledge(msg)
        self.logger.send(f"allocator-{self.tenant}: allocated job {customer.jobid}, customer {customer.user} and suppliers {suppliers}".encode("utf-8"))

    def register(self):
        # blockchain shenanigans
        return 0




