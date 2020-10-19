import pulsar
import threading
import time
import uuid
from bin import app_allocator, app_customer, app_supplier, app_verifier

NUM_EACH = 3
SUPPLIER_PROBS = [0.0 for x in range(NUM_EACH)] + [0.2 for x in range(NUM_EACH)] + [0.4 for x in range(NUM_EACH)] + [0.6 for x in range(NUM_EACH)] + [0.8 for x in range(NUM_EACH)] + [1.0 for x in range(NUM_EACH)]
CUSTOMER_PROBS = [0.0 for x in range(NUM_EACH)] + [0.2 for x in range(NUM_EACH)] + [0.4 for x in range(NUM_EACH)] + [0.6 for x in range(NUM_EACH)] + [0.8 for x in range(NUM_EACH)] + [1.0 for x in range(NUM_EACH)]
SIMNUM = 12
NUMJOBS = 100
START_BALANCE = 1000

if __name__=="__main__":
    threads = []
    a = threading.Thread(target=app_allocator.run)
    threads.append(a)
    a.start()

    # start verifier
    time.sleep(5)
    v = threading.Thread(target=app_verifier.run, args=(f"v-{SIMNUM}",))
    threads.append(v)
    v.start()

    # start suppliers
    for i in range(len(SUPPLIER_PROBS)):
        time.sleep(1.5)
        behavior_probability = SUPPLIER_PROBS[i]
        user = f"s-{SIMNUM}-{i}-{behavior_probability}"
        t = threading.Thread(target=app_supplier.run, args=(user, START_BALANCE, behavior_probability))
        threads.append(t)
        t.start()

    # start customers
    for i in range(len(CUSTOMER_PROBS)):
        time.sleep(2)
        behavior_probability = CUSTOMER_PROBS[i]
        user = f"c-{SIMNUM}-{i}-{behavior_probability}"
        t = threading.Thread(target=app_supplier.run, args=(user, START_BALANCE, behavior_probability, NUMJOBS))
        threads.append(t)
        t.start()




