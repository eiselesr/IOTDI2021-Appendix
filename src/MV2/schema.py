import pulsar


class OfferSchema(pulsar.schema.Record):
    user = pulsar.schema.String()
    replicas = pulsar.schema.Integer()
    allocationid = pulsar.schema.String()
    customerbehavior = pulsar.schema.String()
    b = pulsar.schema.Float()
    lam = pulsar.schema.Integer()
    pi_s = pulsar.schema.Float()
    supplierbehavior = pulsar.schema.String()


class AllocationSchema(pulsar.schema.Record):
    customer = pulsar.schema.String()
    replicas = pulsar.schema.Integer()
    allocationid = pulsar.schema.String()
    customerbehavior = pulsar.schema.String()
    b = pulsar.schema.Float()
    lam = pulsar.schema.Integer()
    pi_s = pulsar.schema.Float()
    supplier = pulsar.schema.String()
    supplierbehavior = pulsar.schema.String()
    outcome = pulsar.schema.String()
    mediator = pulsar.schema.String()


class PayoutSchema(pulsar.schema.Record):
    customer = pulsar.schema.String()
    supplier = pulsar.schema.String()
    customerpay = pulsar.schema.Float()
    supplierpay = pulsar.schema.Float()
    mediatorpay = pulsar.schema.Float()
    outcome = pulsar.schema.String()
    allocationid = pulsar.schema.String()
    customerbehavior = pulsar.schema.String()
    supplierbehavior = pulsar.schema.String()
    payoutid = pulsar.schema.String()


class TransactionSchema(pulsar.schema.Record):
    user = pulsar.schema.String()
    change = pulsar.schema.Float()
    balance = pulsar.schema.Float()
    payoutid = pulsar.schema.String()






