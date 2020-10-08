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

        self.client = pulsar.Client(cfg.pulsar_url)

        topic = f"{cfg.tenant}/{cfg.namespace}/{cfg.logger_topic}"
        self.logger = self.client.create_producer(topic=topic)

        topic = f"persistent://{cfg.tenant}/{cfg.namespace}/allocation_topic"
        self.producer = self.client.create_producer(topic=topic,
                                                schema=pulsar.schema.JsonSchema(schema.AllocationSchema))

        topic = re.compile(f"persistent://{cfg.tenant}/{cfg.namespace}/.*_offers")
        self.consumer = self.client.subscribe(topic=topic,
                                              schema=pulsar.schema.JsonSchema(schema.OfferSchema),
                                              subscription_name="offer-sub",
                                              initial_position=pulsar.InitialPosition.Earliest,
                                              message_listener=self.listener)
        self.logger.send(f"allocator: done initializing allocator".encode("utf-8"))




    def listener(self, consumer, msg):
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        self.logger.send(f"allocator: got a an offer with topic_name {msg.topic_name()}".encode("utf-8"))
        if "customer" in msg.topic_name():
            self.customer_offers.append(msg.value())

        if "supply" in msg.topic_name():
            self.supplier_offers.append(msg.value())

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
                    customer=customer.user,
                    suppliers=suppliers,
                    start=customer.start,
                    end=customer.end,
                    service_name=customer.service_name,
                    price=customer.price,
                    replicas=customer.replicas,
                    num_messages=customer.num_messages)
                self.producer.send(allocation, event_timestamp=int(datetime.datetime.timestamp(now)))
                self.logger.send(f"allocator: allocated job {customer.jobid}, customer {customer.user} and suppliers {suppliers}".encode("utf-8"))
        consumer.acknowledge(msg)

    def register(self):
        # blockchain shenanigans
        return 0




