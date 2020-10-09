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
    def __init__(self, tenant, behavior, start_time, end_time):
        self.id = self.register()
        self.tenant = tenant
        self.behavior = behavior
        self.start_time = start_time
        self.end_time = end_time
        self.output_producer = None

        # create tenant
        PulsarREST.create_tenant(pulsar_admin_url=cfg.pulsar_admin_url, tenant=self.tenant)

        # get client
        self.client = pulsar.Client(cfg.pulsar_url)

        # producer - logger
        self.logger = self.client.create_producer(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/{cfg.logger_topic}")
        self.logger.send(f"supplier-{self.tenant}: initializing".encode("utf-8"))

        # producer - supply offers
        self.supply_offers_producer = self.client.create_producer(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/supply_offers",
                                                                  schema=pulsar.schema.JsonSchema(schema.OfferSchema))

        # consumer - allocation topic
        self.allocation_consumer = self.client.subscribe(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/allocation_topic",
                                                         schema=pulsar.schema.JsonSchema(schema.AllocationSchema),
                                                         subscription_name="allocation{}".format(tenant),
                                                         initial_position=pulsar.InitialPosition.Earliest,
                                                         consumer_type=pulsar.ConsumerType.Exclusive)

    ### public methods ###

    def run(self):
        while time.time() < self.end_time:
            # post offer
            self.post_offer()

            # get allocation
            allocation = self.get_allocation()

            # producer - output
            self.output_producer = self.client.create_producer(topic=f"persistent://{self.tenant}/{allocation.service_name}/output-{allocation.allocationid}")

            # consumer - input
            input_consumer = self.client.subscribe(topic=f"persistent://{allocation.customer}/{allocation.service_name}/input-{allocation.allocationid}",
                                                   subscription_name=f"supplier-{self.tenant}-{allocation.allocationid}",
                                                   initial_position=pulsar.InitialPosition.Earliest,
                                                   consumer_type=pulsar.ConsumerType.Exclusive,
                                                   message_listener=self.process_message)

            # consumer - check
            check_consumer = self.client.subscribe(topic=f"persistent://{allocation.customer}/{allocation.service_name}/check",
                                                   schema=pulsar.schema.JsonSchema(schema.Check),
                                                   subscription_name=f"check-{self.tenant}-{allocation.allocationid}",
                                                   initial_position=pulsar.InitialPosition.Earliest,
                                                   consumer_type=pulsar.ConsumerType.Exclusive)

            # block on check
            while True:
                try:
                    timeout = (cfg.window+100000) * 1000
                    msg = check_consumer.receive(timeout_millis=timeout)
                    check_consumer.acknowledge(msg)
                    if (msg.allocationid == allocation.allocationid) and (msg.status == "done"):
                        self.logger.send(f"supplier-{self.tenant}: got done message from verifier for job {allocation.allocationid}".encode("utf-8"))
                        break
                except:
                    if time.time() >= allocation.end:
                        self.logger.send(f"supplier-{self.tenant}: timeout for {allocation.allocationid}".encode("utf-8"))
                        break

            # job is done, closeout
            check_consumer.close()
            time.sleep(5)
            input_consumer.close()
            self.output_producer.close()
            self.output_producer = None
            self.logger.send(f"supplier-{self.tenant}: done with job allocationid-{allocation.allocationid}".encode("utf-8"))
        self.logger.send(f"supplier-{self.tenant}: run time over, shutting down".encode("utf-8"))

    def post_offer(self):
        offer = schema.OfferSchema(
            allocationid="NA",
            start=0.0,
            end=0.0,
            service_name="NA",
            user=self.tenant,
            account="wallet",
            cpu=1E9,
            rate=1,
            price=0.000001,
            replicas=-1
        )
        properties = {"content-type": "application/json"}
        self.supply_offers_producer.send(offer, properties)
        self.logger.send(f"supplier-{self.tenant}: sent an offer".encode("utf-8"))

    def get_allocation(self):
        while True:
            msg = self.allocation_consumer.receive()
            if self.tenant in msg.value().suppliers:
                self.logger.send(f"supplier-{self.tenant}: got an allocation for jobid {msg.value().jobid}".encode("utf-8"))
                return msg

    def process_message(self, consumer, msg):
        properties = {"msg-num": msg.properties()['msg-num']}
        if self.behavior == "correct":
            result = msg.data()
        else:
            result = str(random.randint(0, 10)).encode("utf-8")
        self.output_producer.send(result, properties=properties)
        self.logger.send(f"supplier-{self.tenant}: published result {result} this value is {self.behavior}".encode("utf-8"))
        consumer.acknowledge(msg)

    def close(self):
        self.client.close()

    def register(self):
        # blockchain shenanigans
        return 0


    ### void

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