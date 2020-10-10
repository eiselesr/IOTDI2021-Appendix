import pulsar


class OfferSchema(pulsar.schema.Record):
    allocationid = pulsar.schema.String()
    start = pulsar.schema.Float()
    end = pulsar.schema.Float()
    service_name = pulsar.schema.String()
    user = pulsar.schema.String()
    account = pulsar.schema.String()
    cpu = pulsar.schema.Float()
    rate = pulsar.schema.Integer()
    price = pulsar.schema.Float()
    replicas = pulsar.schema.Integer()


class AllocationSchema(pulsar.schema.Record):
    allocationid = pulsar.schema.String()
    customer = pulsar.schema.String()
    suppliers = pulsar.schema.Array(pulsar.schema.String())
    start = pulsar.schema.Float()
    end = pulsar.schema.Float()
    service_name = pulsar.schema.String()
    price = pulsar.schema.Float()
    replicas = pulsar.schema.Integer()


class VerifierSchema(pulsar.schema.Record):
    result = pulsar.schema.String()
    customer = pulsar.schema.String()
    suppliers = pulsar.schema.Array(pulsar.schema.String())
    service_name = pulsar.schema.String()
    window = pulsar.schema.Integer()
    num_messages = pulsar.schema.Integer()

class CheckSchema(pulsar.schema.Record):
    result = pulsar.schema.String()
    status = pulsar.schema.String()
    startmessage = pulsar.schema.Integer()
    endmessage = pulsar.schema.Integer()
    allocationid = pulsar.schema.String()



