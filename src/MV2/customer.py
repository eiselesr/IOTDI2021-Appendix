import time
import datetime
import pulsar
import PulsarREST
import cfg
import schema


class Fulfillment(pulsar.Function):
    def __init__(self):
        pass

    def process(self, input, context):
        pass


class Trader:
    def __init__(self, tenant):
        self.id = self.register()
        self.tenant = tenant

        client = pulsar.Client(cfg.pulsar_url)
        allocation_topic = f"persistent://{cfg.tenant}/{cfg.namespace}/allocation_topic"

        # WHY DOES COMMENTING THIS OUT CAUSE THE CONNECTION TO CLOSE?
        self.subscriber = client.subscribe(allocation_topic,
                                           schema=pulsar.schema.JsonSchema(schema.AllocationSchema),
                                           subscription_name="allocation{}".format(tenant),
                                           initial_position=pulsar.InitialPosition.Earliest,
                                           consumer_type=pulsar.ConsumerType.Exclusive)

        # offer_topic = f"persistent://{cfg.tenant}/{cfg.namespace}/customer_offers"
        offer_topic = "customer_offers"
        self.producer = client.create_producer(topic=offer_topic,
                                               schema=pulsar.schema.JsonSchema(schema.CustomerOfferSchema))

    def register(self):
        # blockchain shenanigans
        return 0

    def post_offer(self, oid, replicas=1):

        now = datetime.datetime.now(tz=datetime.timezone.utc)
        start = now + datetime.timedelta(minutes=15)
        end = now + datetime.timedelta(days=1)

        # offer = self.OfferSchema(
        offer = schema.CustomerOfferSchema(
            oid=oid,
            start=int(datetime.datetime.timestamp(start)),
            end=int(datetime.datetime.timestamp(end)),
            service_name="traffic_detection",
            user=self.tenant,
            account="wallet",
            cpu=1E7,
            rate=60,  # per second
            price=0.000001,
            replicas=replicas
        )

        properties = {"content-type": "application/json"}

        self.producer.send(offer, properties, event_timestamp=int(datetime.datetime.timestamp(now)))

    def read_allocation(self):
        pass





if __name__ == "__main__":
    print((datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=15) - datetime.datetime(1970, 1, 1,tzinfo=datetime.timezone.utc)).total_seconds())
    t = datetime.datetime.timestamp(datetime.datetime.now(tz=datetime.timezone.utc)) + 15*60
    print(int(t))
    # print(datetime.datetime.fromtimestamp(t, tz=datetime.timezone.utc))
    print(t)