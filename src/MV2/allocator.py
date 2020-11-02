import re
import uuid
import datetime
import pulsar
import time
import pandas as pd
from . import PulsarREST, cfg, schema


# class Fulfillment(pulsar.Function):
class Allocator:
    def __init__(self):
        self.id = self.register()
        #self.customer_offers = []
        self.customer_offers = pd.DataFrame(columns=['jobid',
                                                     'start',
                                                     'end',
                                                     'service_name',
                                                     'user',
                                                     'account',
                                                     'cpu',
                                                     'rate',
                                                     'price',
                                                     'replicas',
                                                     'timestamp',
                                                     'allocationid',
                                                     'offerid'])
        self.supplier_offers = []

        # pulsar client
        self.client = pulsar.Client(cfg.pulsar_url)

        # producer - logger
        self.logger = self.client.create_producer(topic=f"{cfg.tenant}/{cfg.namespace}/{cfg.logger_topic}")
        self.logger.send(f"allocator: initializing".encode("utf-8"))

        # producer - allocation
        self.allocation_producer = self.client.create_producer(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/allocation_topic",
                                                               schema=pulsar.schema.JsonSchema(schema.AllocationSchema))

        # consumer - supply and customer offers
        self.customer_offer_consumer = self.client.subscribe(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/customer_offers",
                                                             schema=pulsar.schema.JsonSchema(schema.OfferSchema),
                                                             subscription_name="customer-offer-sub-2",
                                                             initial_position=pulsar.InitialPosition.Latest,
                                                             message_listener=self.customer_offer_listener)

        self.supplier_offer_consumer = self.client.subscribe(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/supply_offers",
                                                             schema=pulsar.schema.JsonSchema(schema.OfferSchema),
                                                             subscription_name="supplier-offer-sub-2",
                                                             initial_position=pulsar.InitialPosition.Latest,
                                                             message_listener=self.supply_offer_listener)
        while True:
            time.sleep(0.1)

    def customer_offer_listener(self, consumer, msg):
        consumer.acknowledge(msg)
        self.logger.send(f"allocator: got a an offer with topic_name {msg.topic_name()}".encode("utf-8"))
        data = {'jobid': msg.value().jobid,
                'start': msg.value().start,
                'end': msg.value().end,
                'service_name': msg.value().service_name,
                'user': msg.value().user,
                'account': msg.value().account,
                'cpu': msg.value().cpu,
                'rate': msg.value().rate,
                'price': msg.value().price,
                'replicas': msg.value().replicas,
                'timestamp': msg.value().timestamp,
                'allocationid': msg.value().allocationid,
                'offerid': msg.value().offerid}
        self.customer_offers = self.customer_offers.append(data, ignore_index=True)
        self.allocate()

    def supply_offer_listener(self, consumer, msg):
        consumer.acknowledge(msg)
        self.logger.send(f"allocator: got a an offer with topic_name {msg.topic_name()}".encode("utf-8"))
        self.supplier_offers.append(msg.value())
        self.allocate()

    def allocate(self):
        # see if there is a match
        #print(self.customer_offers.head())
        self.customer_offers = self.customer_offers.sort_values(by='start', ascending=True)
        while len(self.customer_offers) > 0:
            num_replicas_needed = self.customer_offers.iloc[0].replicas
            #print(num_replicas_needed)
            if len(self.supplier_offers) >= num_replicas_needed:
                customer = self.customer_offers.iloc[0]
                #print(customer)
                self.customer_offers = self.customer_offers.iloc[1:]
                suppliers = []
                supplierofferids = []
                supplieroffertimestamps = []
                supplierbehaviors = []
                for i in range(customer.replicas):
                    supplier = self.supplier_offers.pop(0)
                    suppliers.append(supplier.user)
                    supplierofferids.append(supplier.offerid)
                    supplieroffertimestamps.append(supplier.timestamp)
                    supplierbehaviors.append(supplier.supplierbehavior)
                allocation = schema.AllocationSchema(
                    jobid=str(customer.jobid),
                    allocationid=str(customer.allocationid),
                    customer=str(customer.user),
                    suppliers=suppliers,
                    start=float(customer.start),
                    end=float(customer.end),
                    service_name=customer.service_name,
                    price=float(customer.price),
                    replicas=int(customer.replicas),
                    timestamp=time.time(),
                    customerofferid=customer.offerid,
                    supplierofferids=supplierofferids,
                    customeroffertimestamp=float(customer.timestamp),
                    supplieroffertimestamps=supplieroffertimestamps,
                    supplierbehaviors=supplierbehaviors)
                self.allocation_producer.send(allocation)
                self.logger.send(f"allocator: allocated job {customer.allocationid}, customer {customer.user} and suppliers {suppliers}".encode("utf-8"))
            else:
                break

    def register(self):
        # blockchain shenanigans
        return 0




