import time
import argparse
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

    parser.add_argument("-s",
                        "--sleep_btw_offers",
                        help="sleep time in seconds between offers",
                        default='1')


    args = parser.parse_args()

    c = customer.Trader(tenant=args.tenant)

    time.sleep(5)

    for seqnum in range(int(args.num_windows)):
        c.post_offer(seqnum=seqnum,
                     service_name=args.service_name,
                     replicas=int(args.replicas))
        msg = c.get_allocation()
        c.send_data(msg, args.num_messages)
        time.sleep(int(args.sleep_btw_offers))
