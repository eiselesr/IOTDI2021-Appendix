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
        self.service = ""
        self.count = 0
        self.seqnum = 0

        client = pulsar.Client(cfg.pulsar_url)
        # allocation_topic = f"persistent://{cfg.tenant}/{cfg.namespace}/allocation"

        self.consumer = client.subscribe(re.compile(f"persistent://{cfg.tenant}/{cfg.namespace}/.*_offers"),
                                         schema=pulsar.schema.JsonSchema(schema.OfferSchema),
                                         subscription_name="offer-sub",
                                         initial_position=pulsar.InitialPosition.Latest,
                                         message_listener=self.listener)

        self.producer = client.create_producer(topic="allocation_topic",
                                               schema=pulsar.schema.JsonSchema(schema.AllocationSchema))

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
                    seqnum=self.seqnum,
                    customer=customer.user,
                    suppliers=suppliers,
                    start=customer.start,
                    end=customer.end,
                    service_name=customer.service_name,
                    price=customer.price,
                    uuid=str(uuid.uuid4()),
                    num_messages=customer.num_messages)
                self.producer.send(allocation, event_timestamp=int(datetime.datetime.timestamp(now)))
        consumer.acknowledge(msg)

    def register(self):
        # blockchain shenanigans
        return 0




