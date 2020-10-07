import pulsar


class OfferSchema(pulsar.schema.Record):
    jobid = pulsar.schema.String()
    start = pulsar.schema.Integer()
    end = pulsar.schema.Integer()
    service_name = pulsar.schema.String()
    user = pulsar.schema.String()
    account = pulsar.schema.String()
    cpu = pulsar.schema.Float()
    rate = pulsar.schema.Integer()
    price = pulsar.schema.Float()
    replicas = pulsar.schema.Integer()
    num_messages = pulsar.schema.Integer()


class AllocationSchema(pulsar.schema.Record):
    jobid = pulsar.schema.String()
    customer = pulsar.schema.String()
    suppliers = pulsar.schema.Array(pulsar.schema.String())
    start = pulsar.schema.Integer()
    end = pulsar.schema.Integer()
    service_name = pulsar.schema.String()
    price = pulsar.schema.Float()
    num_messages = pulsar.schema.Integer()
    replicas = pulsar.schema.Integer()


class Verifier(pulsar.schema.Record):
    result = pulsar.schema.String()
    customer = pulsar.schema.String()
    suppliers = pulsar.schema.Array(pulsar.schema.String())
    service_name = pulsar.schema.String()
    window = pulsar.schema.Integer()
    num_messages = pulsar.schema.Integer()



