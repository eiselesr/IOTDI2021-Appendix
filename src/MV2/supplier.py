import time
import json
import datetime
import pulsar
import random
from . import PulsarREST, cfg, schema


class Trader:
    def __init__(self,
                 user,
                 balance,
                 behavior_probability=.5):
        self.user = user
        self.balance = balance
        self.behavior_probability = behavior_probability

        # pulsar client
        self.client = pulsar.Client(cfg.pulsar_url)

        # producer - logger
        self.logger = self.client.create_producer(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/{cfg.logger_topic}")
        self.logger.send(f"supplier-{self.user}: initializing".encode("utf-8"))

        # producer - supply offers
        self.supply_offers_producer = self.client.create_producer(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/supply_offers",
                                                                  schema=pulsar.schema.JsonSchema(schema.OfferSchema))

        # producer - transactions
        self.transactions_producer = self.client.create_producer(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/transactions",
                                                                 schema=pulsar.schema.JsonSchema(schema.TransactionSchema))

        # subscribe - payouts
        self.payout_consumer = self.client.subscribe(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/payouts",
                                                     schema=pulsar.schema.JsonSchema(schema.PayoutSchema),
                                                     subscription_name=f"{self.user}-payouts-subscription",
                                                     initial_position=pulsar.InitialPosition.Latest,
                                                     consumer_type=pulsar.ConsumerType.Exclusive,
                                                     message_listener=self.payout_listener)

    def close(self):
        self.client.close()

    def payout_listener(self, consumer, msg):
        consumer.acknowledge(msg)
        if msg.value().supplier == self.user:
            self.balance += msg.value().supplierpay
            data = schema.TransactionSchema(
                user=self.user,
                change=msg.value().supplierpay,
                balance=self.balance,
                payoutid=msg.value().payoutid
            )
            self.transactions_producer.send(data)

    def post_offer(self):
        offer = schema.OfferSchema(
            user=self.user,
            replicas=-1,
            allocationid="NA",
            customerbehavior="NA",
            b=float(-1),
            lam=-1,
            pi_s=float(-1),
            supplierbehavior=self.behavior()
        )
        self.supply_offers_producer.send(offer, properties={"content-type": "application/json"})
        self.logger.send(f"supplier-{self.user}: sent job offer offer".encode("utf-8"))

    def behavior(self):
        if random.random() > self.behavior_probability:
            return "cheat"
        else:
            return "process"