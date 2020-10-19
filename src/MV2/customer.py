import time
import datetime
import pulsar
import random
import uuid
from copy import deepcopy
from . import schema, cfg, PulsarREST


class Trader:
    def __init__(self,
                 user,
                 balance,
                 b,
                 pi_s,
                 lam,
                 replicas,
                 behavior_probability=.5,
                 num_jobs=10):
        self.user = user
        self.balance = balance
        self.behavior_probability = behavior_probability
        self.b = b
        self.pi_s = pi_s
        self.lam = lam
        self.replicas = replicas
        self.num_jobs = num_jobs

        # pulsar client
        self.client = pulsar.Client(cfg.pulsar_url)

        # producer - logger
        self.logger = self.client.create_producer(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/{cfg.logger_topic}")
        self.logger.send(f"customer-{self.user}: initializing".encode("utf-8"))

        # producer - customer_offers
        self.customer_offers_producer = self.client.create_producer(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/customer_offers",
                                                                    schema=pulsar.schema.JsonSchema(schema.OfferSchema))

        # producer - transactions
        self.transactions_producer = self.client.create_producer(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/transactions",
                                                                schema=pulsar.schema.JsonSchema(schema.TransactionSchema))

        # subscribe - payouts
        self.payout_consumer = self.client.subscribe(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/payouts",
                                                     schema=pulsar.schema.JsonSchema(schema.PayoutSchema),
                                                     subscription_name=f"{self.user}-payouts-subscription",
                                                     initial_position=pulsar.InitialPosition.Latest,
                                                     consumer_type=pulsar.ConsumerType.Exclusive)

        count = 0
        while count < self.num_jobs:
            self.post_offer()
            self.get_payout()
            count += 1
            if self.balance <= 0:
                break
        self.close()


    def close(self):
        self.client.close()

    def get_payout(self):
        while True:
            msg = self.payout_consumer.receive()
            self.payout_consumer.acknowledge(msg)
            if msg.value().customer == self.user:
                self.balance += msg.value().customerpay
                data = schema.TransactionSchema(
                    user=self.user,
                    change=msg.value().customerpay,
                    balance=self.balance,
                    payoutid=msg.value().payoutid
                )
                self.transactions_producer.send(data)
                break

    def post_offer(self):
        allocationid = str(uuid.uuid4())
        offer = schema.OfferSchema(
            user=self.user,
            replicas=self.replicas,
            allocationid=allocationid,
            customerbehavior=self.behavior(),
            b=self.b,
            lam=self.lam,
            pi_s=self.pi_s,
            supplierbehavior="NA"
        )
        self.customer_offers_producer.send(offer, properties={"content-type": "application/json"})
        self.logger.send(f"customer-{self.user}: sent job offer on with allocationid {allocationid}".encode("utf-8"))

    def behavior(self):
        if random.random() > self.behavior_probability:
            return "cheat"
        else:
            return "process"

