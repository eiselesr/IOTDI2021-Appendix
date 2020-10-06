import time
import json
import datetime
import pulsar
import random
from . import PulsarREST, cfg, schema


class Fulfillment(pulsar.Function):
    def __init__(self):
        pass

    def process(self, input, context):
        pass


class Trader:
    def __init__(self, tenant, seed):
        self.id = self.register()
        self.tenant = tenant

        self.client = pulsar.Client(cfg.pulsar_url)
        allocation_topic = f"persistent://{cfg.tenant}/{cfg.namespace}/allocation_topic"

        PulsarREST.create_tenant(pulsar_admin_url=cfg.pulsar_admin_url, tenant=tenant)

        # WHY DOES COMMENTING THIS OUT CAUSE THE CONNECTION TO CLOSE?
        self.allocation_consumer = self.client.subscribe(allocation_topic,
                                              schema=pulsar.schema.JsonSchema(schema.AllocationSchema),
                                              subscription_name="allocation{}".format(tenant),
                                              initial_position=pulsar.InitialPosition.Earliest,
                                              consumer_type=pulsar.ConsumerType.Exclusive)

        # In exclusive mode, only a single consumer is allowed to attach
        # to the subscription. If multiple consumers subscribe to a topic
        # using the same subscription, an error occurs.
        # https://pulsar.apache.org/docs/en/concepts-messaging/

        offer_topic = f"persistent://{cfg.tenant}/{cfg.namespace}/supply_offers"
        self.supply_offers_producer = self.client.create_producer(topic=offer_topic,
                                                    schema=pulsar.schema.JsonSchema(schema.OfferSchema))

    ### public methods ###

    def post_offer(self):
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        start = now + datetime.timedelta(minutes=15)
        end = now + datetime.timedelta(days=1)
        offer = schema.SupplierOfferSchema(
            seqnum=-1,
            start=int(datetime.datetime.timestamp(start)),
            end=int(datetime.datetime.timestamp(end)),
            service_name="NA",
            user=self.tenant,
            account="wallet",
            cpu=1E9,
            rate=1,
            price=0.000001,
            replicas=-1,
            num_messages=-1
        )
        properties = {"content-type": "application/json"}
        self.supply_offers_producer.send(offer, properties, event_timestamp=int(datetime.datetime.timestamp(now)))

    def get_allocation(self):
        while True:
            msg = self.allocation_consumer.receive()
            if self.tenant in msg.value().suppliers:
                return msg

    def do_job(self, msg):
        service_name = msg.value().service_name
        seqnum = msg.value().seqnum
        input_tenant = msg.value().customer
        num_messages = msg.value().num_messages

        PulsarREST.create_namespace(pulsar_admin_url=cfg.pulsar_admin_url, tenant=self.tenant, namespace=service_name)
        service_output = "persistent://{}/{}/{}".format(self.tenant, service_name, seqnum)
        producer = self.client.create_producer(topic=service_output)

        # get the data
        service_input = "persistent://{}/{}/{}".format(input_tenant, service_name, seqnum)
        job_consumer = self.client.subscribe(service_input,
                                             initial_position=pulsar.InitialPosition.Earliest,
                                             consumer_type=pulsar.ConsumerType.Exclusive,
                                             subscription_name=f"{self.tenant}_{service_name}_{seqnum}")

        result = random.choice(["correct", "cheat", "fault"])
        for i in range(num_messages):
            data = int(job_consumer.receive().data().decode("utf-8"))
            if result == "correct":
                producer.send(str(data).decode("utf-8"))
            elif result == "cheat":
                producer.send(str(random.randint(0, 10)).decode("utf-8"))
            else:
                continue


    ### private methods###

    def register(self):
        # blockchain shenanigans
        return 0

    def create_function(self):

        tenant = "public"
        namespace = "default"
        className = "ReadInput"
        functionName = "ReadInput"

        api_url = f"http://localhost:8080/admin/v3/functions/{tenant}/{namespace}/{functionName}"
        function_path = f"/home/ubuntu/projects/MODiCuM-Streaming/src/MV2/PulsarFunctions/{functionName}.py"


        print(pulsar.schema.BytesSchema())

        config = {"tenant": f"{tenant}",
                  "namespace": f"{namespace}",
                  "name": functionName,
                  "className": f"{className}.{functionName}",
                  "inputs": [f"persistent://{tenant}/{namespace}/fubar"],
                  "output": f"persistent://{tenant}/{namespace}/frobaz",
                  # "outputSchemaType": "BYTES",
                  "outputSerdeClassName": f"{className}.BytesSerDe",
                  "forwardSourceMessageProperty": True,
                  "userConfig": {},
                  "py": function_path}

        print(config)

        # PulsarREST.create_function(api_url, config, function_path)
        PulsarREST.update_function(api_url, config, function_path)

        PulsarREST.get_functions()