import time
import datetime
import pulsar
import random
import uuid
from copy import deepcopy
from . import schema, cfg, PulsarREST


class Trader:
    def __init__(self,
                 jobid,
                 start,
                 end,
                 service_name,
                 user,
                 account="wallet",
                 cpu=1E7,
                 rate=60,
                 price=0.000001,
                 replicas=2):
        self.jobid = jobid
        self.start = start
        self.end = end
        self.service_name = service_name
        self.user = user
        self.account = account
        self.cpu = cpu
        self.rate = rate
        self.price = price
        self.replicas = replicas

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
        self.input_producer = self.client.create_producer(topic=f"persistent://{self.tenant}/{self.service_name}/input",
                                                          schema=pulsar.schema.JsonSchema(schema.InputDataSchema))

        # post offers
        self.post_all_offers()

        # stream data
        self.stream_data()

    ### public methods ###

    def stream_data(self):
        self.logger.send(f"customer-{self.user}: start sending data for service_name: {self.service_name}, jobid: {self.jobid}".encode("utf-8"))
        while time.time() < self.end:
            if time.time() >= self.start:
                data = schema.InputDataSchema(
                    value=random.randint(1, 10),
                    customer=self.user,
                    service_name=self.service_name,
                    jobid=self.jobid,
                    start=self.start,
                    end=self.end,
                    timestamp=time.time()
                )
                self.input_producer.send(data, properties={"content-type": "application/json"})
            time.sleep(1)
        self.logger.send(f"customer-{self.user}: done sending data for service_name: {self.service_name}, jobid: {self.jobid}".encode("utf-8"))
        self.input_producer.close()

    def close(self):
        self.client.close()

    ### private methods ###

    def post_all_offers(self):
        self.logger.send(f"customer-{self.user}: starting to send offers on service_name: {self.service_name}, jobid: {self.jobid}".encode("utf-8"))
        window_start = deepcopy(self.start)
        while window_start < self.end:
            window_end = window_start + cfg.window
            allocationid = str(uuid.uuid4())
            self.post_offer(allocationid, window_start, window_end)
            window_start = deepcopy(window_end)
        self.logger.send(f"customer-{self.user}: done sending offers on service_name: {self.service_name}, jobid: {self.jobid}".encode("utf-8"))

    def post_offer(self, allocationid, window_start, window_end):
        offer = schema.OfferSchema(
            jobid=self.jobid,
            start=window_start,
            end=window_end,
            service_name=self.service_name,
            user=self.user,
            account=self.account,
            cpu=self.cpu,
            rate=self.rate,
            price=self.price,
            replicas=self.replicas,
            timestamp=time.time(),
            allocationid=allocationid
        )
        self.customer_offers_producer.send(offer, properties={"content-type": "application/json"})
        self.logger.send(f"customer-{self.user}: sent job offer on service_name: {self.service_name}, jobid: {self.jobid}, allocationid: {allocationid}".encode("utf-8"))

