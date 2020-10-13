import pulsar


class OfferSchema(pulsar.schema.Record):
    jobid = pulsar.schema.String()
    start = pulsar.schema.Float()
    end = pulsar.schema.Float()
    service_name = pulsar.schema.String()
    user = pulsar.schema.String()
    account = pulsar.schema.String()
    cpu = pulsar.schema.Float()
    rate = pulsar.schema.Integer()
    price = pulsar.schema.Float()
    replicas = pulsar.schema.Integer()
    timestamp = pulsar.schema.Float()
    allocationid = pulsar.schema.String()


class AllocationSchema(pulsar.schema.Record):
    jobid = pulsar.schema.String()
    allocationid = pulsar.schema.String()
    customer = pulsar.schema.String()
    suppliers = pulsar.schema.Array(pulsar.schema.String())
    start = pulsar.schema.Float()
    end = pulsar.schema.Float()
    service_name = pulsar.schema.String()
    price = pulsar.schema.Float()
    replicas = pulsar.schema.Integer()
    timestamp = pulsar.schema.Float()


class CheckSchema(pulsar.schema.Record):
    result = pulsar.schema.String()
    customer = pulsar.schema.String()
    suppliers = pulsar.schema.Array(pulsar.schema.String())
    service_name = pulsar.schema.String()
    jobid = pulsar.schema.String()
    allocationid = pulsar.schema.String()
    timestamp = pulsar.schema.Float()


class InputDataSchema(pulsar.schema.Record):
    value = pulsar.schema.Integer()
    customer = pulsar.schema.String()
    service_name = pulsar.schema.String()
    jobid = pulsar.schema.String()
    start = pulsar.schema.Float()
    end = pulsar.schema.Float()
    timestamp = pulsar.schema.Float()
    msgnum = pulsar.schema.Integer()


class OutputDataSchema(pulsar.schema.Record):
    value = pulsar.schema.Integer()
    customer = pulsar.schema.String()
    service_name = pulsar.schema.String()
    jobid = pulsar.schema.String()
    start = pulsar.schema.Float()
    end = pulsar.schema.Float()
    supplier = pulsar.schema.String()
    allocationid = pulsar.schema.String()
    timestamp = pulsar.schema.Float()
    msgnum = pulsar.schema.Integer()



