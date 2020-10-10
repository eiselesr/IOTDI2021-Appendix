import time
import datetime
import pulsar
import random
import uuid
from copy import deepcopy
from . import schema, cfg, PulsarREST


class Fulfillment(pulsar.Function):
    def __init__(self):
        pass

    def process(self, input, context):
        pass


class Trader:
    def __init__(self,
                 tenant,
                 replicas,
                 service_name,
                 start_time,
                 end_time):
        self.tenant = tenant
        self.replicas = replicas
        self.service_name = service_name
        self.start_time = start_time
        self.end_time = end_time
        self.msg_num = 0

        # register tenant and namespace with Pulsar
        PulsarREST.create_tenant(pulsar_admin_url=cfg.pulsar_admin_url, tenant=self.tenant)
        PulsarREST.create_namespace(pulsar_admin_url=cfg.pulsar_admin_url, tenant=self.tenant, namespace=self.service_name)

        # get pulsar client
        self.client = pulsar.Client(cfg.pulsar_url)

        # producer - logger
        self.logger = self.client.create_producer(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/{cfg.logger_topic}")
        self.logger.send(f"customer-{self.tenant}: initializing".encode("utf-8"))

        # producer - customer_offers
        self.customer_offers_producer = self.client.create_producer(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/customer_offers",
                                                                    schema=pulsar.schema.JsonSchema(schema.OfferSchema))

        # producer - input
        self.input_producer = self.client.create_producer(topic=f"persistent://{self.tenant}/{self.service_name}/input")

        # consumer - output
        self.output_consumer = self.client.subscribe(topic=f"persistent://{self.tenant}/{self.service_name}/output",
                                                     subscription_name=f"{self.tenant}-{self.service_name}-output-print",
                                                     initial_position=pulsar.InitialPosition.Latest,
                                                     consumer_type=pulsar.ConsumerType.Exclusive,
                                                     message_listener=self.print_listener)

    ### public methods ###

    def run(self):
        window_start = time.time()
        while window_start < self.end_time:
            window_end = window_start + cfg.window
            allocationid = str(uuid.uuid4())
            self.post_offer(allocationid, window_start, window_end)
            self.stream_data(window_start, window_end, allocationid)
            window_start = time.time()
        self.logger.send(f"customer-{self.tenant}: job is done, shutting down".encode("utf-8"))

    def stream_data(self, window_start, window_end, allocationid):
        self.logger.send(f"customer-{self.tenant}: start sending data for ".encode("utf-8"))
        #input_producer = self.client.create_producer(topic=f"persistent://{self.tenant}/{self.service_name}/input-{allocationid}")
        while time.time() <= window_end:
            if time.time() >= window_start:
                input_producer.send(str(random.randint(1, 10)).encode("utf-8"),
                                    properties={"timestamp": str(time.time()),
                                                "msg-num": str(self.msg_num)})
                self.msg_num += 1
                time.sleep(.1)
        self.logger.send(f"customer-{self.tenant}: ending sending data for allocationid {allocationid}, msg-num: {self.msg_num}".encode("utf-8"))
        input_producer.close()

    def close(self):
        self.client.close()

    ### private methods ###

    def post_offer(self, allocationid, window_start, window_end):
        # build offer
        offer = schema.OfferSchema(
            allocationid=allocationid,
            start=window_start,
            end=window_end,
            service_name=self.service_name,
            user=self.tenant,
            account="wallet",
            cpu=1E7,
            rate=60,  # per second
            price=0.000001,
            replicas=self.replicas
        )
        self.customer_offers_producer.send(offer,
                                           properties={"content-type": "application/json",
                                                       "timestamp": str(time.time())})
        self.logger.send(f"customer-{self.tenant}: posted offer with allocationid {allocationid}".encode("utf-8"))

    def print_listener(self, consumer, msg):
        message = f"customer-{self.tenant}: got result from output topic, result={msg.value()}, msg-num={msg.properties()['msg-num']}"
        print(message)
        self.logger.send(message.encode("utf-8"))
        consumer.acknowledge(msg)

    def read_allocation(self):
        pass

    def register(self):
        # blockchain shenanigans
        return 0

