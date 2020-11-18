import pulsar
import threading
import time
import uuid
import random
from bin import app_allocator, app_customer, app_supplier, app_verifier, app_mediator


NUM_SUPPLIERS = 30
NUM_CUSTOMERS = 10
SIMNUM = 1
service_name = "rand_nums"

if __name__=="__main__":
    # start allocator
    threads = []
    a = threading.Thread(target=app_allocator.run)
    threads.append(a)
    a.start()

    # start verifier
    time.sleep(5)
    v = threading.Thread(target=app_verifier.run, args=(f"v{SIMNUM}",))
    threads.append(v)
    v.start()

    # start mediator
    time.sleep(5)
    m = threading.Thread(target=app_mediator.run, args=(f"m{SIMNUM}",))
    m.start()

    time.sleep(2)
    start = time.time() + 120
    end = start + 800
    for i in range(NUM_SUPPLIERS):
        user = f"s-{SIMNUM}-{i}"
        behavior = "correct"
        t = threading.Thread(target=app_supplier.run, args=(user, start, end, behavior))
        threads.append(t)
        t.start()
    print("done starting suppliers at time {}".format(time.time()))

    # start customers
    time.sleep(1)
    for i in range(NUM_CUSTOMERS):
        #time.sleep(1)
        jobid = str(uuid.uuid4())
        user = f"c-{SIMNUM}-{i}"
        replicas = 1
        c = threading.Thread(target=app_customer.run, args=(jobid, start, end, service_name, user, replicas))
        threads.append(c)
        c.start()

    print(f"system started at: {time.time()}")