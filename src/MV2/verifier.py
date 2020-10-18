import pulsar
import pandas as pd
import time
import threading
from copy import deepcopy
from . import cfg, schema, PulsarREST, queries, game


class Verifier:
    def __init__(self, user="verifier"):
        self.user = user
        self.df_allocations = pd.DataFrame(columns=["customer",
                                                    "replicas",
                                                    "allocationid",
                                                    "customerbehavior",
                                                    "b",
                                                    "lam",
                                                    "pi_s",
                                                    "supplier",
                                                    "supplierbehavior",
                                                    "payoutid"])

        # pulsar client
        self.client = pulsar.Client(cfg.pulsar_url)

        # producer - logger
        self.logger = self.client.create_producer(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/{cfg.logger_topic}")
        self.logger.send(f"verifier-{self.user}: initializing".encode("utf-8"))

        # producer - payouts
        self.payouts_producer = self.client.create_producer(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/payouts",
                                                            schema=pulsar.schema.JsonSchema(schema.PayoutSchema))

        # subscribe - allocations
        self.allocation_consumer = self.client.subscribe(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/allocation_topic",
                                                         schema=pulsar.schema.JsonSchema(schema.PayoutSchema),
                                                         subscription_name=f"{self.user}-allocation-subscription",
                                                         initial_position=pulsar.InitialPosition.Latest,
                                                         consumer_type=pulsar.ConsumerType.Exclusive,
                                                         message_listener=self.allocation_listener)

        # periodically check for expired allocations
        while True:
            t = threading.Thread(target=self.flush_allocations)
            t.start()
            t.join()

    def allocation_listener(self, consumer, msg):
        consumer.acknowledge(msg)
        data = {"customer": msg.value().customer,
                "replicas": msg.value().replicas,
                "allocationid": msg.value().allocationid,
                "customerbehavior": msg.value().customerbehavior,
                "b": msg.value().b,
                "lam": msg.value().lam,
                "pi_s": msg.value().pi_s,
                "supplier": msg.value().supplier,
                "supplierbehavior": msg.value().supplierbehavior,
                "payoutid": msg.value().payoutid}
        self.df_allocations.append(data, ignore_index=True)

    def flush_allocations(self):
        time.sleep(5)
        df = deepcopy(self.df_allocations)
        if len(df) > 0:
            allocations_to_remove = []
            for allocationid in df['allocationid'].unique():
                allocation = df[df['allocationid']==allocationid]
                if len(allocation) == allocation['replicas'].tolist()[0]:
                    allocations_to_remove.append(allocationid)
                    self.payout(allocation)
            self.df_allocations = self.df_allocations[~self.df_allocations['allocationid'].isin(allocations_to_remove)]
            self.logger.send(f"verifier: verified allocations {allocations_to_remove}".encode("utf-8"))

    def payout(self, allocation):
        for k, v in allocation.iterrows():
            data = schema.PayoutSchema(
                customer=v['customer'],
                supplier=v['supplier'],
                customerpay=game.get_customer_pay(v),
                supplierpay=game.get_supplier_pay(v),
                mediatorpay=game.get_mediator_pay(v),
                allocatorpay=game.get_allocator_pay(v),
                outcome=game.get_game_outcome(v),
                allocationid=v['allocationid'],
                customerbehavior=v['customerbehavior'],
                supplierbehavior=v['supplierbehavior'],
                payoutid=v['payoutid']
            )
            self.payouts_producer.send(data)
