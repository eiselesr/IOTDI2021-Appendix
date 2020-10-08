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
        self.tenant = tenant
        PulsarREST.create_tenant(pulsar_admin_url=cfg.pulsar_admin_url, tenant=self.tenant)

        self.client = pulsar.Client(cfg.pulsar_url)
        self.logger = self.client.create_producer(topic=f"{cfg.tenant}/{cfg.namespace}/{cfg.logger_topic}")

        # customer offers producer
        offer_topic = f"persistent://{cfg.tenant}/{cfg.namespace}/customer_offers"
        self.customer_offers_producer = self.client.create_producer(topic=offer_topic,
                                                                    schema=pulsar.schema.JsonSchema(schema.OfferSchema))

        # allocation consumer
        allocation_topic = f"persistent://{cfg.tenant}/{cfg.namespace}/allocation_topic"
        self.allocation_consumer = self.client.subscribe(allocation_topic,
                                                         schema=pulsar.schema.JsonSchema(schema.AllocationSchema),
                                                         subscription_name="allocation{}".format(tenant),
                                                         initial_position=pulsar.InitialPosition.Earliest,
                                                         consumer_type=pulsar.ConsumerType.Exclusive)
        self.logger.send(f"customer-{self.tenant}: done initializing customer".encode("utf-8"))




### public methods ###

    def post_offer(self, jobid, service_name, num_messages, replicas=1):

        now = datetime.datetime.now(tz=datetime.timezone.utc)
        start = now + datetime.timedelta(minutes=15)
        end = now + datetime.timedelta(days=1)

        # offer = self.OfferSchema(
        offer = schema.OfferSchema(
            jobid=jobid,
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
        self.logger.send(f"customer-{self.tenant}: posted offer with jobid {jobid}".encode("utf-8"))

    def get_allocation(self):
        while True:
            msg = self.allocation_consumer.receive()
            if self.tenant == msg.value().customer:
                self.logger.send(f"customer-{self.tenant}: got allocation for job {msg.value().jobid}, will be supplied by {msg.value().suppliers}".encode("utf-8"))
                return msg

    def send_data(self, msg, num_messages):
        PulsarREST.create_namespace(pulsar_admin_url=cfg.pulsar_admin_url, tenant=self.tenant, namespace=msg.value().service_name)
        input_topic = f"persistent://{self.tenant}/{msg.value().service_name}/{msg.value().jobid}"
        input_producer = self.client.create_producer(topic=input_topic)

        for i in range(int(num_messages)):
            data = str(random.randint(1, 10))
            input_producer.send(data.encode("utf-8"))
        self.logger.send(f"customer-{self.tenant}: sent {num_messages} for jobid {msg.value().jobid}, done sending messages".encode("utf-8"))
        input_producer.close()

    def retrieve_result(self, service_name, jobid, num_messages):
        c = self.client.subscribe(topic=f"persistent://{self.tenant}/{service_name}/{jobid}-output", subscription_name=f"results-{self.tenant}-{jobid}")
        counter = 0
        while True:
            result = str(c.receive().data().decode("utf-8"))
            counter += 1
            self.logger.send(f"customer-{self.tenant}: got result {result}")
            if (result == "job failed") or counter >= num_messages:
                break
        c.close()

    def close(self):
        self.client.close()

    ### private methods ###

    def read_allocation(self):
        pass

    def register(self):
        # blockchain shenanigans
        return 0

