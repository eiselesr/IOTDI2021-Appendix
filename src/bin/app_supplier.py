import os
import time
import argparse
from MV2 import *


def run(user, start, end, behavior):
    s = supplier.Trader(user=user,
                        start=start,
                        end=end,
                        behavior=behavior)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="supplier")

    parser.add_argument("-s",
                        "--start",
                        help="start time",
                        default="none")

    parser.add_argument("-e",
                        "--end",
                        help="end time",
                        default="none")

    parser.add_argument("-u",
                        "--user",
                        help="tenant",
                        default="s1")

    parser.add_argument("-b",
                        "--behavior",
                        help="correct or fail",
                        default="correct")

    args = parser.parse_args()

    if args.start=="none":
        start = time.time() + 30
    else:
        start = float(args.start)

    if args.end=="none":
        end = start + 600
    else:
        end = float(args.end)

    run(user=args.user, start=start, end=end, behavior=args.behavior)
