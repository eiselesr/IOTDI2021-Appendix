import pulsar
import threading
import time
import uuid
import random
from bin import app_allocator, app_customer, app_supplier, app_verifier


NUM_SUPPLIERS = 30
NUM_CUSTOMERS = 30
SIMNUM = 1

if __name__=="__main__":
    threads = []
    a = threading.Thread(target=app_allocator.run)
    threads.append(a)
    a.start()

    # start verifier
    time.sleep(5)
    v = threading.Thread(target=app_verifier.run, args=(f"v{SIMNUM}",))
    threads.append(v)
    v.start()

    time.sleep(10)

    supplier_count, customer_count = 0, 0
    while (supplier_count < NUM_SUPPLIERS) or (customer_count < NUM_CUSTOMERS):
        entity = random.choice(['customer', 'supplier'])
        if (entity == 'customer') and (customer_count < NUM_CUSTOMERS):
            user = f"c-{SIMNUM}-{customer_count}"
            jobid = str(uuid.uuid4())
            start = time.time() + 25
            end = start + 1000
            service_name = "rand_nums"
            replicas = 1
            c = threading.Thread(target=app_customer.run, args=(jobid, start, end, service_name, user, replicas))
            threads.append(c)
            c.start()
            customer_count += 1
        elif (entity == "supplier") and (supplier_count < NUM_SUPPLIERS):
            user = f"s-{SIMNUM}-{supplier_count}"
            behavior = "correct"
            t = threading.Thread(target=app_supplier.run, args=(user, start, end, behavior))
            threads.append(t)
            t.start()
            supplier_count += 1
    print(f"system started at: {time.time()}")




