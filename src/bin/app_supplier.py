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
                        help="start time in seconds",
                        default="none")

    parser.add_argument("-et",
                        "--end_time",
                        help="end time in seconds",
                        default="none")


    args = parser.parse_args()

    if args.start_time=="none":
        start_time = time.time()
    else:
        start_time = float(args.start_time)

    if args.end_time=="none":
        end_time = time.time() + 600
    else:
        end_time = float(args.end_time)

    s = supplier.Trader(tenant=args.tenant,
                        behavior=args.behavior,
                        start_time=start_time,
                        end_time=end_time)

    s.run()
    s.close()