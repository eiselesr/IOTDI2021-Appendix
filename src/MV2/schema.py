import pulsar


class OfferSchema(pulsar.schema.Record):
    user = pulsar.schema.String()
    replicas = pulsar.schema.Integer()
    allocationid = pulsar.schema.String()
    customerbehavior = pulsar.schema.String()
    supplierbehavior = pulsar.schema.String()
    customerbehaviorprob = pulsar.schema.Float()
    supplierbehaviorprob = pulsar.schema.Float()


class AllocationSchema(pulsar.schema.Record):
    customer = pulsar.schema.String()
    replicas = pulsar.schema.Integer()
    allocationid = pulsar.schema.String()
    customerbehavior = pulsar.schema.String()
    supplier = pulsar.schema.String()
    supplierbehavior = pulsar.schema.String()
    payoutid = pulsar.schema.String()
    customerbehaviorprob = pulsar.schema.Float()
    supplierbehaviorprob = pulsar.schema.Float()


class PayoutSchema(pulsar.schema.Record):
    customer = pulsar.schema.String()
    supplier = pulsar.schema.String()
    customerpay = pulsar.schema.Float()
    supplierpay = pulsar.schema.Float()
    mediatorpay = pulsar.schema.Float()
    allocatorpay = pulsar.schema.Float()
    outcome = pulsar.schema.String()
    allocationid = pulsar.schema.String()
    customerbehavior = pulsar.schema.String()
    supplierbehavior = pulsar.schema.String()
    payoutid = pulsar.schema.String()
    customerbehaviorprob = pulsar.schema.Float()
    supplierbehaviorprob = pulsar.schema.Float()


class TransactionSchema(pulsar.schema.Record):
    user = pulsar.schema.String()
    change = pulsar.schema.Float()
    balance = pulsar.schema.Float()
    payoutid = pulsar.schema.String()






