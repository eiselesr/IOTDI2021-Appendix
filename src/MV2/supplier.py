import time
import json
import datetime
import pulsar
import PulsarREST
import cfg
import schema
import random


class Fulfillment(pulsar.Function):
    def __init__(self):
        pass

    def process(self, input, context):
        pass


class Trader:
    def __init__(self, tenant, seed):
        self.id = self.register()
        self.tenant = tenant
        self.received_messages = []
        self.seed = seed

        self.client = pulsar.Client(cfg.pulsar_url)
        allocation_topic = f"persistent://{cfg.tenant}/{cfg.namespace}/allocation_topic"

        PulsarREST.create_tenant(pulsar_admin_url=cfg.pulsar_admin_url, tenant=tenant)

        # WHY DOES COMMENTING THIS OUT CAUSE THE CONNECTION TO CLOSE?
        self.subscriber = self.client.subscribe(allocation_topic,
                                           schema=pulsar.schema.JsonSchema(schema.AllocationSchema),
                                           subscription_name="allocation{}".format(tenant),
                                           initial_position=pulsar.InitialPosition.Earliest,
                                           consumer_type=pulsar.ConsumerType.Exclusive,
                                           message_listener=self.listener)
        # In exclusive mode, only a single consumer is allowed to attach
        # to the subscription. If multiple consumers subscribe to a topic
        # using the same subscription, an error occurs.
        # https://pulsar.apache.org/docs/en/concepts-messaging/

        # offer_topic = f"persistent://{cfg.tenant}/{cfg.namespace}/supply_offers"
        offer_topic = "supply_offers"
        self.producer = self.client.create_producer(topic=offer_topic,
                                                    schema=pulsar.schema.JsonSchema(schema.SupplierOfferSchema))

    def process(self, input, context=None):
        if self.tenant in input.value().suppliers:
            service = input.value().service_name
            print(service)
            PulsarREST.create_namespace(pulsar_admin_url=cfg.pulsar_admin_url, tenant=self.tenant, namespace=service)
            service_input = "persistent://{}/{}/input{}".format(self.tenant, service, input.value().uuid)
            service_output = "persistent://{}/{}/output{}".format(self.tenant, service, input.value().uuid)
            producer = self.client.create_producer(topic=service_output)

            print("{}: DO THE JOB".format(self.tenant))
            random.seed(self.seed)
            for i in range(10):
                result = random.choice(["correct", "cheat", "fault"])
                # print(result)
                properties = {"tenant": self.tenant, "sequence_id": str(i), "encoding": "utf-8"}

                producer.send(result.encode(properties["encoding"]), properties=properties, sequence_id=i)
                # producer.send(result.encode(properties["encoding"]), sequence_id=i)

                # data
                # event_timestamp
                # message_id
                # partition_key
                # properties
                # publish_timestamp
                # redelivery_count
                # topic_name
                # value

                # send(content, properties=None, partition_key=None,
                #      sequence_id=None, replication_clusters=None,
                #      disable_replication=False, event_timestamp=None,
                #      deliver_at=None, deliver_after=None)
            # TODO - DELETE NAMESPACE WHEN DONE
            return True
        else:
            return False


    def listener(self, consumer, msg):
        data = self.process(msg)
        # print(f"Listener: {data}")
        if data:
            print("{}: DID THE JOB".format(self.tenant))
        else:
            print("{}: NOT MY JOB".format(self.tenant))

        self.received_messages.append(msg)
        consumer.acknowledge(msg)

    def register(self):
        # blockchain shenanigans
        return 0

    def post_offer(self, oid):

        now = datetime.datetime.now(tz=datetime.timezone.utc)
        start = now + datetime.timedelta(minutes=15)
        end = now + datetime.timedelta(days=1)

        # offer = self.OfferSchema(
        offer = schema.SupplierOfferSchema(
            oid=oid,
            start=int(datetime.datetime.timestamp(start)),
            end=int(datetime.datetime.timestamp(end)),
            service_name="NA",
            user=self.tenant,
            account="wallet",
            cpu=1E9,
            rate=1,
            price=0.000001,
            replicas=1
        )

        properties = {"content-type": "application/json"}

        self.producer.send(offer, properties, event_timestamp=int(datetime.datetime.timestamp(now)))

    def read_allocation(self):
        pass


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