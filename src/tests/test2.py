import pulsar
import threading
import time
import random
from MV2 import PulsarREST, cfg
from bin import app_allocator, app_customer, app_supplier, app_verifier

#SIMNUM = 1
TENANT = "public"


NUMJOBS = 1000
REPLICAS = 1
START_BALANCE = float(1000)
SUPPLIER_PROBS = [0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
CUSTOMER_PROBS = [0.0, 0.25, 0.5, 0.75, 1.0, 1.1]
THREADS = []

def run_sim(namespace, supplier_prob, simnum):
    PulsarREST.create_namespace(pulsar_admin_url=cfg.pulsar_admin_url,
                                tenant=TENANT,
                                namespace=namespace)

    time.sleep(5)
    print(f"created namespace for {namespace}")

    a = threading.Thread(target=app_allocator.run, args=(START_BALANCE, namespace))
    THREADS.append(a)
    a.start()
    print(f"started allocator for {namespace}")


    # start verifier
    time.sleep(5)
    v = threading.Thread(target=app_verifier.run, args=(f"v-{namespace}", namespace))
    THREADS.append(v)
    v.start()
    print(f"started verifier for {namespace}")

    # create 8 suppliers
    for i in range(9):
        user = f"s-{namespace}-{i}"
        t = threading.Thread(target=app_supplier.run, args=(user, START_BALANCE, supplier_prob, namespace))
        THREADS.append(t)
        t.start()
    print("started suppliers")

    # start customers
    for i in range(len(CUSTOMER_PROBS)):
        time.sleep(1)
        behavior_probability = CUSTOMER_PROBS[i]
        user = f"c-{namespace}-{i}"
        t = threading.Thread(target=app_customer.run, args=(user, START_BALANCE, REPLICAS, behavior_probability, NUMJOBS, namespace, simnum, supplier_prob))
        THREADS.append(t)
        t.start()
    print("started customers")


if __name__=="__main__":
    for i in range(len(SUPPLIER_PROBS)):
        namespace = f"sim-{i}"
        supplier_prob = SUPPLIER_PROBS[i]
        run_sim(namespace=namespace, supplier_prob=supplier_prob, simnum=i)
        time.sleep(5)