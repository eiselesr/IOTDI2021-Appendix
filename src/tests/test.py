import time
import pulsar
from MV2 import *
from bin.app_customer import run_customer

if __name__=="__main__":
    tenant = 'c1'
    replicas = '2'
    num_windows = '3'
    service_name = 'test'
    sleep_btw_offers = '1'

    run_customer(tenant, replicas, num_windows, service_name, sleep_btw_offers)

    # get results
    time.sleep(10)

    client = pulsar.Client(cfg.pulsar_url)

    # test offers
    offer_topic = f"persistent://{cfg.tenant}/{cfg.namespace}/customer_offers"

    # test allocation
    allocation_topic = f"persistent://{cfg.tenant}/{cfg.namespace}/allocation_topic"


    for seqnum in range(int(num_windows)):
        input_topic = f"persistent://{tenant}/{service_name}/{seqnum}"


