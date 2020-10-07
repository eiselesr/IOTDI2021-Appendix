import os
import time
import argparse
from MV2 import *


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="supplier")

    parser.add_argument("-t",
                        "--tenant",
                        help="tenant",
                        default='s1')

    parser.add_argument("-b",
                        "--behavior",
                        help="correct or cheat",
                        default='correct')


    args = parser.parse_args()

    s = supplier.Trader(tenant=args.tenant,
                        behavior=args.behavior)

    time.sleep(5)

    while True:
        s.post_offer()
        msg = s.get_allocation()
        s.do_job(msg)
        time.sleep(5)
    s.close()