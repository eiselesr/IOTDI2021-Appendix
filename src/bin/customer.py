import os
os.chdir(os.path.join(os.getcwd(), "MV2"))
import customer
import time
import argparse


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="customer")

    parser.add_argument("-t",
                        "--tenant",
                        help="tenant",
                        default='sh1')

    parser.add_argument("-r",
                        "--replicas",
                        help="number of replicas",
                        default='2')

    parser.add_argument("-o",
                        "--oid",
                        help="offer id",
                        default='0')

    parser.add_argument("-n",
                        "--number_of_offers",
                        help="number of offers",
                        default='1')

    parser.add_argument("-s",
                        "--sleep_btw_offers",
                        help="sleep time in seconds between offers",
                        default='1')


    args = parser.parse_args()

    c = customer.Trader(tenant=args.tenant)

    time.sleep(5)
    replicas = int(args.replicas)
    number_of_offers = int(args.number_of_offers)
    sleep_btw_offers = int(args.sleep_btw_offers)
    oid = int(args.oid)
    for offer in range(oid, number_of_offers+oid):
        c.post_offer(oid=offer, replicas=replicas)
        time.sleep(sleep_btw_offers)