import pulsar
import threading
import time
import uuid
from MV2 import PulsarREST, cfg
from bin import app_allocator, app_customer, app_supplier, app_verifier

SIMNUM = 1
tenant = "public"

NUM_EACH = 5
SUPPLIER_PROBS = [0.0 for x in range(NUM_EACH)] + [0.2 for x in range(NUM_EACH)] + [0.4 for x in range(NUM_EACH)] + [0.6 for x in range(NUM_EACH)] + [0.8 for x in range(NUM_EACH)] + [1.0 for x in range(NUM_EACH)]
CUSTOMER_PROBS = [0.0 for x in range(NUM_EACH)] + [0.2 for x in range(NUM_EACH)] + [0.4 for x in range(NUM_EACH)] + [0.6 for x in range(NUM_EACH)] + [0.8 for x in range(NUM_EACH)] + [1.0 for x in range(NUM_EACH)]
NUMJOBS = 100
REPLICAS = 1
START_BALANCE = float(1000)

if __name__=="__main__":
    threads = []
    # register tenant and namespace with Pulsar
    PulsarREST.create_tenant(pulsar_admin_url=cfg.pulsar_admin_url,
                             tenant=tenant)
    PulsarREST.create_namespace(pulsar_admin_url=cfg.pulsar_admin_url,
                                tenant=tenant,
                                namespace=cfg.namespace)

    time.sleep(5)
    print(f"created tenant: {tenant}")

    a = threading.Thread(target=app_allocator.run, args=(START_BALANCE,))
    threads.append(a)
    a.start()
    print("started allocator")


    # start verifier
    time.sleep(5)
    v = threading.Thread(target=app_verifier.run, args=(f"v-{SIMNUM}",))
    threads.append(v)
    v.start()
    print("started verifier")

    # start suppliers
    for i in range(len(SUPPLIER_PROBS)):
        time.sleep(1.5)
        behavior_probability = SUPPLIER_PROBS[i]
        user = f"s-{SIMNUM}-{i}"
        t = threading.Thread(target=app_supplier.run, args=(user, START_BALANCE, behavior_probability))
        threads.append(t)
        t.start()
    print("started suppliers")

    # start customers
    for i in range(len(CUSTOMER_PROBS)):
        time.sleep(2)
        behavior_probability = CUSTOMER_PROBS[i]
        user = f"c-{SIMNUM}-{i}"
        t = threading.Thread(target=app_customer.run, args=(user, START_BALANCE, REPLICAS, behavior_probability, NUMJOBS))
        threads.append(t)
        t.start()
    print("started customers")




