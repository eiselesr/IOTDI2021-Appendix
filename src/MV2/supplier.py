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
    def __init__(self, tenant, behavior):
        self.id = self.register()
        self.tenant = tenant
        PulsarREST.create_tenant(pulsar_admin_url=cfg.pulsar_admin_url, tenant=self.tenant)
        self.behavior = behavior

        self.client = pulsar.Client(cfg.pulsar_url)
        self.logger = self.client.create_producer(topic=f"{cfg.tenant}/{cfg.namespace}/{cfg.logger_topic}")

        offer_topic = f"persistent://{cfg.tenant}/{cfg.namespace}/supply_offers"
        self.supply_offers_producer = self.client.create_producer(topic=offer_topic,
                                                              schema=pulsar.schema.JsonSchema(schema.OfferSchema))

        allocation_topic = f"persistent://{cfg.tenant}/{cfg.namespace}/allocation_topic"
        self.allocation_consumer = self.client.subscribe(allocation_topic,
                                              schema=pulsar.schema.JsonSchema(schema.AllocationSchema),
                                              subscription_name="allocation{}".format(tenant),
                                              initial_position=pulsar.InitialPosition.Earliest,
                                              consumer_type=pulsar.ConsumerType.Exclusive)
        self.logger.send(f"supplier-{self.tenant}: done initializing supplier I will be {self.behavior}".encode("utf-8"))




    ### public methods ###

    def post_offer(self):
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        start = now + datetime.timedelta(minutes=15)
        end = now + datetime.timedelta(days=1)
        offer = schema.OfferSchema(
            jobid="NA",
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
        self.logger.send(f"supplier-{self.tenant}: sent an offer".encode("utf-8"))

    def get_allocation(self):
        while True:
            msg = self.allocation_consumer.receive()
            if self.tenant in msg.value().suppliers:
                PulsarREST.create_namespace(pulsar_admin_url=cfg.pulsar_admin_url, tenant=self.tenant, namespace=msg.value().service_name)
                self.logger.send(f"supplier-{self.tenant}: got an allocation for jobid {msg.value().jobid}".encode("utf-8"))
                return msg

    def do_job(self, msg):
        # TODO move to get allocation
        service_output = f"persistent://{self.tenant}/{msg.value().service_name}/{msg.value().jobid}"
        producer = self.client.create_producer(topic=service_output)

        # TODO move to allocation
        # get the data
        service_input = f"persistent://{msg.value().customer}/{msg.value().service_name}/{msg.value().jobid}"
        job_consumer = self.client.subscribe(service_input,
                                             initial_position=pulsar.InitialPosition.Earliest,
                                             consumer_type=pulsar.ConsumerType.Exclusive,
                                             subscription_name=f"{self.tenant}_{msg.value().service_name}_{msg.value().jobid}")

        # do_job
        properties = {"jobid": msg.value().jobid, 'supplier': self.tenant}
        for i in range(msg.value().num_messages):
            data = job_consumer.receive()
            if self.behavior == "correct":
                producer.send(data.data(), properties=properties)
            else:
                producer.send(str(random.randint(0, 10)).encode("utf-8"), properties=properties)
        self.logger.send(f"supplier-{self.tenant}: done doing job {msg.value().jobid}".encode("utf-8"))
        producer.close()

    def close(self):
        self.client.close()


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