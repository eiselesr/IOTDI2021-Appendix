import time
import argparse
import uuid
from MV2 import *


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="customer")

    parser.add_argument("-t",
                        "--tenant",
                        help="tenant",
                        default='c1')

    parser.add_argument("-r",
                        "--replicas",
                        help="number of replicas",
                        default='2')

    parser.add_argument("-a",
                        "--service_name",
                        help="name of service",
                        default='traffic_analyzer')

    parser.add_argument("-n",
                        "--num_windows",
                        help="number of windows",
                        default='5')

    parser.add_argument("-m",
                        "--num_messages",
                        help="number of messages",
                        default='10')


    args = parser.parse_args()

    c = customer.Trader(tenant=args.tenant)

    time.sleep(5)

    for window in range(int(args.num_windows)):
        jobid = str(uuid.uuid4())
        c.post_offer(jobid=jobid,
                     service_name=args.service_name,
                     num_messages=int(args.num_messages),
                     replicas=int(args.replicas))
        msg = c.get_allocation()
        c.send_data(msg, args.num_messages)
        c.retrieve_result(args.service_name, jobid, int(args.num_messages))
        time.sleep(5)
    c.close()
