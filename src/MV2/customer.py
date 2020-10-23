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
                 replicas,
                 behavior_probability,
                 num_jobs,
                 namespace=None,
                 simnum=None,
                 supplierprob=None):
        self.transnum = 0
        self.user = user
        self.balance = balance
        self.behavior_probability = behavior_probability
        self.replicas = replicas
        self.num_jobs = num_jobs

        if namespace is None:
            self.namespace = cfg.namespace
        else:
            self.namespace = namespace
        if simnum is None:
            self.simnum = -1
        else:
            self.simnum = simnum

        if supplierprob is None:
            self.supplierprob = -1
        else:
            self.supplierprob = supplierprob

        # pulsar client
        self.client = pulsar.Client(cfg.pulsar_url)

        # producer - logger
        self.logger = self.client.create_producer(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/{cfg.logger_topic}")
        self.logger.send(f"customer-{self.user}: initializing".encode("utf-8"))

        # producer - customer_offers
        self.customer_offers_producer = self.client.create_producer(topic=f"persistent://{cfg.tenant}/{self.namespace}/customer_offers",
                                                                    schema=pulsar.schema.JsonSchema(schema.OfferSchema))

        # producer - transactions
        self.transactions_producer = self.client.create_producer(topic=f"persistent://{cfg.tenant}/{self.namespace}/transactions",
                                                                schema=pulsar.schema.JsonSchema(schema.TransactionSchema))

        # subscribe - payouts
        self.payout_consumer = self.client.subscribe(topic=f"persistent://{cfg.tenant}/{self.namespace}/payouts",
                                                     schema=pulsar.schema.JsonSchema(schema.PayoutSchema),
                                                     subscription_name=f"{self.user}-payouts-subscription",
                                                     initial_position=pulsar.InitialPosition.Latest,
                                                     consumer_type=pulsar.ConsumerType.Exclusive)

        self.count = 0
        while self.count < self.num_jobs:
            if self.count == self.num_jobs-1:
                self.send_summary_message()
            self.post_offer()
            self.get_payout()
            self.count += 1
        # send simulation summary
        #self.send_summary_message()
        self.close()

    def close(self):
        self.client.close()

    def send_summary_message(self):
        data = schema.LastBalance(
            user=self.user,
            balance=self.balance,
            numjobs=self.count,
            behaviorprob=self.behavior_probability,
            entitytype="customer",
            namespace=self.namespace,
            simnum=self.simnum,
            supplierprob=self.supplierprob
        )
        producer = self.client.create_producer(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/last_balance",
                                               schema=pulsar.schema.JsonSchema(schema.LastBalance))
        producer.send(data)


    def get_payout(self):
        while True:
            msg = self.payout_consumer.receive()
            self.payout_consumer.acknowledge(msg)
            if msg.value().customer == self.user:
                self.balance += msg.value().customerpay
                self.transnum += 1
                data = schema.TransactionSchema(
                    user=self.user,
                    change=msg.value().allocatorpay,
                    balance=self.balance,
                    payoutid=msg.value().payoutid,
                    transnum=self.transnum,
                    customer=msg.value().customer,
                    supplier=msg.value().supplier,
                    customerpay=msg.value().customerpay,
                    supplierpay=msg.value().supplierpay,
                    mediatorpay=msg.value().mediatorpay,
                    allocatorpay=msg.value().allocatorpay,
                    outcome=msg.value().outcome,
                    allocationid=msg.value().allocationid,
                    customerbehavior=msg.value().customerbehavior,
                    supplierbehavior=msg.value().supplierbehavior,
                    customerbehaviorprob=msg.value().customerbehaviorprob,
                    supplierbehaviorprob=msg.value().supplierbehaviorprob
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
            supplierbehavior="NA",
            customerbehaviorprob=self.behavior_probability,
            supplierbehaviorprob=-1.0,
        )
        self.customer_offers_producer.send(offer, properties={"content-type": "application/json"})
        self.logger.send(f"customer-{self.user}: sent job offer on with allocationid {allocationid}".encode("utf-8"))

    def behavior(self):
        if random.random() > self.behavior_probability:
            return "cheat"
        else:
            return "process"

