import pulsar


# persistent://{cfg.tenant}/{cfg.namespace}/customer_offers
# persistent://{cfg.tenant}/{cfg.namespace}/supply_offers
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
    offerid = pulsar.schema.String()
    supplierbehavior = pulsar.schema.String()


# persistent://{cfg.tenant}/{cfg.namespace}/allocation_topic
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
    customerofferid = pulsar.schema.String()
    supplierofferids = pulsar.schema.Array(pulsar.schema.String())
    customeroffertimestamp = pulsar.schema.Float()
    supplieroffertimestamps = pulsar.schema.Array(pulsar.schema.Float())
    supplierbehaviors = pulsar.schema.Array(pulsar.schema.String())


# persistent://{customer tenant}/{customer service_name}/check
class CheckSchema(pulsar.schema.Record):
    result = pulsar.schema.String()
    customer = pulsar.schema.String()
    suppliers = pulsar.schema.Array(pulsar.schema.String())
    supplierbehaviors = pulsar.schema.Array(pulsar.schema.String())
    service_name = pulsar.schema.String()
    jobid = pulsar.schema.String()
    allocationid = pulsar.schema.String()
    timestamp = pulsar.schema.Float()


# persistent://{customer tenant}/{customer service_name}/input
class InputDataSchema(pulsar.schema.Record):
    value = pulsar.schema.Integer()
    customer = pulsar.schema.String()
    service_name = pulsar.schema.String()
    jobid = pulsar.schema.String()
    start = pulsar.schema.Float()
    end = pulsar.schema.Float()
    timestamp = pulsar.schema.Float()
    msgnum = pulsar.schema.Integer()


# persistent://{customer tenant}/{customer service_name}/output
class OutputDataSchema(pulsar.schema.Record):
    value = pulsar.schema.Integer()
    customer = pulsar.schema.String()
    service_name = pulsar.schema.String()
    jobid = pulsar.schema.String()
    start = pulsar.schema.Float()
    end = pulsar.schema.Float()
    supplier = pulsar.schema.String()
    allocationid = pulsar.schema.String()
    customertimestamp = pulsar.schema.Float()
    suppliertimestamp = pulsar.schema.Float()
    msgnum = pulsar.schema.Integer()


# persistent://{cfg.tenant}/{customer service_name}/mediation
class MediationSchema(pulsar.schema.Record):
    result = pulsar.schema.String()
    customer = pulsar.schema.String()
    supplierspass = pulsar.schema.Array(pulsar.schema.String())
    suppliersfail = pulsar.schema.Array(pulsar.schema.String())
    service_name = pulsar.schema.String()
    jobid = pulsar.schema.String()
    allocationid = pulsar.schema.String()
    checktimestamp = pulsar.schema.Float()
    mediationtimestamp = pulsar.schema.Float()
