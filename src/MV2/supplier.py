import time
import json
import datetime
import pulsar
import random
import uuid
from . import PulsarREST, cfg, schema


class Fulfillment(pulsar.Function):
    def __init__(self):
        pass

    def process(self, input, context):
        pass


class Trader:
    def __init__(self,
                 user,
                 start,
                 end,
                 account="wallet",
                 cpu=1E9,
                 rate=1,
                 price=0.000001,
                 behavior='correct'):
        self.id = self.register()
        self.user = user
        self.start = start
        self.end = end
        self.account = account
        self.cpu = cpu
        self.rate = rate
        self.price = price
        self.behavior = behavior

        # create tenant
        PulsarREST.create_tenant(pulsar_admin_url=cfg.pulsar_admin_url, tenant=self.user)

        # pulsar client
        self.client = pulsar.Client(cfg.pulsar_url)

        # producer - logger
        self.logger = self.client.create_producer(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/{cfg.logger_topic}")
        self.logger.send(f"supplier-{self.user}: initializing".encode("utf-8"))

        # producer - supply offers
        self.supply_offers_producer = self.client.create_producer(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/supply_offers",
                                                                  schema=pulsar.schema.JsonSchema(schema.OfferSchema))

        # consumer - allocation topic
        self.allocation_consumer = self.client.subscribe(topic=f"persistent://{cfg.tenant}/{cfg.namespace}/allocation_topic",
                                                         schema=pulsar.schema.JsonSchema(schema.AllocationSchema),
                                                         subscription_name=f"{self.user}-allocation-subscription",
                                                         initial_position=pulsar.InitialPosition.Latest,
                                                         consumer_type=pulsar.ConsumerType.Exclusive)

        self.run()

    ### public methods ###

    def run(self):
        while time.time() < self.end:
            # post offer
            self.post_offer()

            # get allocation
            allocation = self.get_allocation()
            self.logger.send(f"supplier-{self.user}: starting allocation {allocation.value().allocationid}".encode("utf-8"))

            # producer - output
            output_producer = self.client.create_producer(topic=f"persistent://{allocation.value().customer}/{allocation.value().service_name}/output",
                                                          schema=pulsar.schema.JsonSchema(schema.OutputDataSchema))

            # consumer - input
            input_consumer = self.client.subscribe(topic=f"persistent://{allocation.value().customer}/{allocation.value().service_name}/input",
                                                   schema=pulsar.schema.JsonSchema(schema.InputDataSchema),
                                                   subscription_name=f"{self.user}-input-{allocation.value().service_name}-{allocation.value().allocationid}",
                                                   initial_position=pulsar.InitialPosition.Latest,
                                                   consumer_type=pulsar.ConsumerType.Exclusive)

            # process messages until allocation is finished
            while True:
                try:
                    msg = input_consumer.receive()
                    if (msg.value().timestamp >= allocation.value().start) and (msg.value().timestamp < allocation.value().end):
                        value = self.process(msg.value().value)

                        output_data = schema.OutputDataSchema(
                            value=value,
                            customer=msg.value().customer,
                            service_name=msg.value().service_name,
                            jobid=msg.value().jobid,
                            start=allocation.value().start,
                            end=allocation.value().end,
                            supplier=self.user,
                            allocationid=allocation.value().allocationid,
                            customertimestamp=msg.value().timestamp,
                            suppliertimestamp=time.time(),
                            msgnum=msg.value().msgnum
                        )
                        output_producer.send(output_data, properties={"content-type": "application/json"})
                    input_consumer.acknowledge(msg)
                    if msg.value().timestamp > allocation.value().end:
                        break
                except Exception as e:
                    ee = repr(e)
                    print(f"supplier-{self.user}: {ee}")
                    self.logger.send(f"supplier-{self.user}: exception when reading input data - {ee}".encode("utf-8"))
                    break
            self.logger.send(f"supplier-{self.user}: finished allocation {allocation.value().allocationid}".encode("utf-8"))
            input_consumer.close()
            output_producer.close()
        self.logger.send(f"supplier-{self.user}: supplier is done, shutting down".encode("utf-8"))
        self.close()

    def post_offer(self):
        offer = schema.OfferSchema(
            jobid="NA",
            start=self.start,
            end=self.end,
            service_name="NA",
            user=self.user,
            account=self.account,
            cpu=self.cpu,
            rate=self.rate,
            price=self.price,
            replicas=-1,
            timestamp=time.time(),
            allocationid="NA",
            offerid=str(uuid.uuid4())
        )
        self.supply_offers_producer.send(offer, {"content-type": "application/json"})
        self.logger.send(f"supplier-{self.user}: sent an offer".encode("utf-8"))

    def get_allocation(self):
        while True:
            msg = self.allocation_consumer.receive()
            self.allocation_consumer.acknowledge(msg)
            if self.user in msg.value().suppliers:
                self.logger.send(f"supplier-{self.user}: got an allocation for allocationid {msg.value().allocationid}".encode("utf-8"))
                return msg

    def process(self, value):
        if self.behavior == 'correct':
            result = value
        else:
            result = str(random.randint(0, 10))
        return result

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