import pulsar

class CustomerOfferSchema(pulsar.schema.Record):
    oid = pulsar.schema.Integer()
    start = pulsar.schema.Integer()
    end = pulsar.schema.Integer()
    service_name = pulsar.schema.String()
    user = pulsar.schema.String()
    account = pulsar.schema.String()
    cpu = pulsar.schema.Float()
    rate = pulsar.schema.Integer()
    price = pulsar.schema.Float()
    replicas = pulsar.schema.Integer()

class SupplierOfferSchema(pulsar.schema.Record):
    oid = pulsar.schema.Integer()
    start = pulsar.schema.Integer()
    end = pulsar.schema.Integer()
    service_name = pulsar.schema.String()
    user = pulsar.schema.String()
    account = pulsar.schema.String()
    cpu = pulsar.schema.Float()
    rate = pulsar.schema.Integer()
    price = pulsar.schema.Float()
    replicas = pulsar.schema.Integer()


class AllocationSchema(pulsar.schema.Record):
    aid = pulsar.schema.Integer()
    customer = pulsar.schema.String()
    suppliers = pulsar.schema.Array(pulsar.schema.String())
    start = pulsar.schema.Integer()
    end = pulsar.schema.Integer()
    service_name = pulsar.schema.String()
    price = pulsar.schema.Float()


