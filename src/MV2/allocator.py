import re
import uuid
import datetime
import pulsar
import PulsarREST
import cfg
import schema


# class Fulfillment(pulsar.Function):
class Allocator:
    def __init__(self):
        self.id = self.register()
        self.received_messages = []
        self.customer_offers = []
        self.supplier_offers = []
        self.service = ""
        self.count = 0
        self.aid = 0

        client = pulsar.Client(cfg.pulsar_url)
        # allocation_topic = f"persistent://{cfg.tenant}/{cfg.namespace}/allocation"

        self.consumer = client.subscribe(re.compile('persistent://public/default/.*_offers'),
                                         schema=pulsar.schema.JsonSchema(schema.CustomerOfferSchema),
                                         subscription_name="offer-sub",
                                         initial_position=pulsar.InitialPosition.Latest,
                                         message_listener=self.listener)

        self.producer = client.create_producer(topic="allocation_topic",
                                               schema=pulsar.schema.JsonSchema(schema.AllocationSchema))



    def process(self, input, context=None):
        print(input.topic_name())
        # TODO - store offers to list and remove when there is one of each
        if "customer" in input.topic_name():
            self.customer_offers.append(input.value())

        if "supply" in input.topic_name():
            self.supplier_offers.append(input.value())

        if self.supplier_offers and self.customer_offers:
            customer = self.customer_offers.pop()
            suppliers = []
            if len(self.supplier_offers) >= customer.replicas:
                self.seqnum += 1
                for i in range(customer.replicas):
                    supplier = self.supplier_offers.pop()
                    suppliers.append(supplier.user)
                allocation = schema.AllocationSchema(
                    seqnum=self.seqnum,
                    customer=customer.user,
                    suppliers=suppliers,
                    start=customer.start,
                    end=customer.end,
                    service_name=customer.service_name,
                    price=customer.price,
                    uuid=str(uuid.uuid4()))
                return allocation
            else:
                self.customer_offers.append(customer)

    def register(self):
        # blockchain shenanigans
        return 0

    def listener(self, consumer, msg):
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        print("GOT OFFER ON: {}".format(msg.topic_name()))
        allocation = self.process(msg)
        self.received_messages.append(msg)
        consumer.acknowledge(msg)
        if allocation:
            self.count += 1
            print("Allocation: {}".format(self.count))
            self.producer.send(allocation, event_timestamp=int(datetime.datetime.timestamp(now)))

    # def receive(self):
    #
    #     while True:
    #         try:
    #             msg = self.consumer.receive(timeout_millis=10000)
    #             data = self.process(msg)
    #             print(data)
    #             self.consumer.acknowledge(msg)
    #         except AttributeError as e:
    #             print(e)
    #             self.consumer.close()
    #             quit()
    #         except Exception as e:
    #             # print(e)
    #             # print(dir(e))
    #             if "TimeOut" in str(e):
    #                 print("the timeout_millis triggered: {}".format(e))
    #             else:
    #                 print("unknown exception")
    #             self.consumer.close()
    #             quit()


if __name__ == "__main__":
    pass