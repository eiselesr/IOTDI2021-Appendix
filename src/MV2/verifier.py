import re
import pulsar
import cfg
import schema

class Verifier:
    def __init__(self, tenant):
        self.received_messages = []
        self.tenant = tenant
        self.client = pulsar.Client(cfg.pulsar_url)

        allocation_topic = f"persistent://{cfg.tenant}/{cfg.namespace}/allocation_topic"
        self.consumer = self.client.subscribe(allocation_topic,
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
        # print(msg.properties())
        # print(msg.message_id())


    def allocation_listener(self, consumer, msg):
        consumer.acknowledge(msg)
        print("this is the allocation: {}".format(msg.value()))

        service_output = []
        service = msg.value().service_name
        sub_name = "{}_{}".format(self.tenant, service)
        for supplier in msg.value().suppliers:
            print("This is the supplier:{}".format(supplier))
            topic = "persistent://{}/{}/{}".format(supplier, service, "output")

            self.client.subscribe(topic,
                                  subscription_name=sub_name,
                                  initial_position=pulsar.InitialPosition.Earliest,
                                  consumer_type=pulsar.ConsumerType.Exclusive,
                                  message_listener=self.result_listener)


