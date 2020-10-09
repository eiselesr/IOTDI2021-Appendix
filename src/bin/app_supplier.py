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

    parser.add_argument("-st",
                        "--start_time",
                        help="start time in seconds")

    parser.add_argument("-et",
                        "--end_time",
                        help="end time in seconds")


    args = parser.parse_args()

    s = supplier.Trader(tenant=args.tenant,
                        behavior=args.behavior,
                        start_time=float(args.start_time),
                        end_time=float(args.end_time))

    s.run()
    s.close()