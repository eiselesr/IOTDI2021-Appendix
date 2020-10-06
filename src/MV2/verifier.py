import re
import pulsar
from . import cfg, schema


class Verifier:
    def __init__(self, tenant):
        self.received_results = {}
        self.tenant = tenant
        self.client = pulsar.Client(cfg.pulsar_url)

        allocation_topic = f"persistent://{cfg.tenant}/{cfg.namespace}/allocation_topic"
        self.allocation_consumer = self.client.subscribe(allocation_topic,
                                                         schema=pulsar.schema.JsonSchema(schema.AllocationSchema),
                                                         subscription_name="allocation{}".format(tenant),
                                                         initial_position=pulsar.InitialPosition.Earliest,
                                                         consumer_type=pulsar.ConsumerType.Exclusive,
                                                         message_listener=self.allocation_listener)

    def process(self, input, context=None):
        pass


    def result_listener(self, consumer, msg):
        consumer.acknowledge(msg)
        print("verifier:{} topic:{} value:{}".format(self.tenant, msg.topic_name(), msg.value()))
        allocation = msg.properties()["allocation_uuid"]
        supplier = msg.properties()["supplier"]
        result = msg.value()
        if allocation not in self.received_results:
            self.received_results[allocation] = allocation
        self.received_results[allocation][supplier] = result
        print(self.received_results)
        # compare the results from allocated suppliers


    def allocation_listener(self, consumer, msg):
        consumer.acknowledge(msg)
        print("this is the allocation: {}".format(msg.value()))

        service = msg.value().service_name
        allocation = "{}_{}".format(service, msg.value().uuid)
        sub_name = "{}_{}".format(self.tenant, allocation)
        for supplier in msg.value().suppliers:
            print("This is the supplier:{}".format(supplier))
            topic = "persistent://{}/{}/output{}".format(supplier, service, msg.value().uuid)


            self.client.subscribe(topic,
                                  subscription_name=sub_name,
                                  initial_position=pulsar.InitialPosition.Earliest,
                                  consumer_type=pulsar.ConsumerType.Exclusive,
                                  message_listener=self.result_listener)

        self.received_results[allocation] = []


