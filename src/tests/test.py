import pulsar
import threading
import time
import uuid
from bin import app_allocator, app_customer, app_supplier, app_verifier


NUM_SUPPLIERS = 5
NUM_CUSTOMERS = 2
SIMNUM = 11

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

    # start suppliers
    start = time.time()
    end = start + 800
    time.sleep(5)
    for i in range(NUM_SUPPLIERS):
        time.sleep(5)
        user = f"s{SIMNUM}{i}"
        behavior = "correct"
        t = threading.Thread(target=app_supplier.run, args=(user, start, end, behavior))
        threads.append(t)
        t.start()

    # start customers
    time.sleep(5)
    for i in range(NUM_CUSTOMERS):
        time.sleep(1)
        jobid = str(uuid.uuid4())
        start = time.time() + 45
        end = start + 200
        service_name = "rand_nums"
        user = f"c{SIMNUM}{i}"
        replicas = 2
        c = threading.Thread(target=app_customer.run, args=(jobid, start, end, service_name, user, replicas))
        threads.append(c)
        c.start()




