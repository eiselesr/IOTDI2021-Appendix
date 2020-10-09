import subprocess
import time
import pulsar
import sys
import re
from MV2 import *


def print_listener(consumer, msg):
    print(f"value: {msg.value()}, msg-num: {msg.properties()['msg-num']}, topic: {consumer.topic()}")
    consumer.acknowledge(msg)


if __name__=="__main__":
    tenant, replicas, service_name, start_time, end_time = "c1", "2", "test_app3", f"{time.time()}", f"{time.time()+60}"

    proc = subprocess.Popen([sys.executable,
                             "bin/app_customer.py",
                             "--tenant", tenant,
                             "--replicas", replicas,
                             "--service_name", service_name,
                             "--start_time", start_time,
                             "--end_time", end_time], stdout=subprocess.PIPE)

    time.sleep(5)
    client = pulsar.Client(cfg.pulsar_url)
    c = client.subscribe(re.compile(f"persistent://{tenant}/{service_name}/input-.*"),
                                subscription_name="test-customer",
                                initial_position=pulsar.InitialPosition.Earliest,
                                consumer_type=pulsar.ConsumerType.Exclusive,
                                message_listener=print_listener)

    if time.time() > end_time:
        print("test done")
        quit()
    #stdout_value = proc.communicate()[0].decode('utf-8')
    #print('stdout:', repr(stdout_value))




