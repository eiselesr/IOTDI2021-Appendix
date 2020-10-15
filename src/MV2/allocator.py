import re
import uuid
import datetime
import pulsar
import time
from . import PulsarREST, cfg, schema, game


class Allocator:
    def __init__(self, balance, user="allocator"):
        self.user = user
        self.balance = balance
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

        # producer - transactions
        self.transactions_producer = self.client.create_producer(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/transactions",
                                                                 schema=pulsar.schema.JsonSchema(schema.TransactionSchema))

        # consumer - supply and customer offers
        self.offer_consumer = self.client.subscribe(topic=re.compile(f"persistent://{cfg.tenant}/{cfg.namespace}/.*_offers"),
                                                    schema=pulsar.schema.JsonSchema(schema.OfferSchema),
                                                    subscription_name="offer-sub-2",
                                                    initial_position=pulsar.InitialPosition.Latest,
                                                    message_listener=self.offer_listener)

        # subscribe - payouts
        self.payout_consumer = self.client.subscribe(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/payouts",
                                                     schema=pulsar.schema.JsonSchema(schema.PayoutSchema),
                                                     subscription_name=f"{self.user}-payouts-subscription",
                                                     initial_position=pulsar.InitialPosition.Latest,
                                                     consumer_type=pulsar.ConsumerType.Exclusive,
                                                     message_listener=self.payout_listener)

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
                for i in range(customer.replicas):
                    supplier = self.supplier_offers.pop(0)
                    allocation = schema.AllocationSchema(
                        customer=customer.user,
                        replicas=customer.replicas,
                        allocationid=customer.allocationid,
                        customerbehavior=customer.customerbehavior,
                        b=customer.b,
                        lam=customer.lam,
                        pi_s=customer.pi_s,
                        supplier=supplier.user,
                        supplierbehavior=supplier.supplierbehavior,
                        payoutid=str(uuid.uuid4())
                    )
                    self.allocation_producer.send(allocation)
                    self.logger.send(f"allocator: allocated job {customer.allocationid}, customer {customer.user} and suppliers {supplier.user}".encode("utf-8"))

    def payout_listener(self, consumer, msg):
        consumer.acknowledge(msg)
        self.balance += msg.value().customerpay
        data = schema.TransactionSchema(
            user=self.user,
            change=msg.value().allocatorpay,
            balance=self.balance,
            payoutid=msg.value().payoutid
        )
        self.transactions_producer.send(data)
