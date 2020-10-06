import time
import datetime
import pulsar
import random
from . import schema, cfg, PulsarREST


class Fulfillment(pulsar.Function):
    def __init__(self):
        pass

    def process(self, input, context):
        pass


class Trader:
    def __init__(self, tenant):
        print("lk")
        self.tenant = tenant
        self.client = pulsar.Client(cfg.pulsar_url)

        # allocation consumer
        allocation_topic = f"persistent://{cfg.tenant}/{cfg.namespace}/allocation_topic"
        self.allocation_consumer = self.client.subscribe(allocation_topic,
                                                         schema=pulsar.schema.JsonSchema(schema.AllocationSchema),
                                                         subscription_name="allocation{}".format(tenant),
                                                         initial_position=pulsar.InitialPosition.Earliest,
                                                         consumer_type=pulsar.ConsumerType.Exclusive)

        # customer offers producer
        offer_topic = f"persistent://{cfg.tenant}/{cfg.namespace}/customer_offers"
        self.customer_offers_producer = self.client.create_producer(topic=offer_topic,
                                                                    schema=pulsar.schema.JsonSchema(schema.OfferSchema))




    ### public methods ###

    def post_offer(self, seqnum, service_name, num_messages, replicas=1):

        now = datetime.datetime.now(tz=datetime.timezone.utc)
        start = now + datetime.timedelta(minutes=15)
        end = now + datetime.timedelta(days=1)

        # offer = self.OfferSchema(
        offer = schema.CustomerOfferSchema(
            seqnum=seqnum,
            start=int(datetime.datetime.timestamp(start)),
            end=int(datetime.datetime.timestamp(end)),
            service_name=service_name,
            user=self.tenant,
            account="wallet",
            cpu=1E7,
            rate=60,  # per second
            price=0.000001,
            replicas=replicas,
            num_messages=num_messages
        )

        properties = {"content-type": "application/json"}

        self.customer_offers_producer.send(offer, properties, event_timestamp=int(datetime.datetime.timestamp(now)))

    def get_allocation(self):
        while True:
            msg = self.allocation_consumer.receive()
            if self.tenant in msg.value().consumers:
                return msg

    def send_data(self, msg, num_messages):
        service_name = msg.value().service_name
        seqnum = msg.value().seqnum
        PulsarREST.create_namespace(pulsar_admin_url=cfg.pulsar_admin_url, tenant=self.tenant, namespace=service_name)
        input_topic = f"persistent://{self.tenant}/{service_name}/{seqnum}"
        input_producer = self.client.create_producer(topic=input_topic)

        for i in range(int(num_messages)):
            data = str(random.randint(1, 10))
            input_producer.send(data.encode("utf-8"))

    def close(self):
        self.client.close()

    ### private methods ###

    def read_allocation(self):
        pass

    def register(self):
        # blockchain shenanigans
        return 0

