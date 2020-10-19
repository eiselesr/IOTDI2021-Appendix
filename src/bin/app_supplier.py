import os
import time
import argparse
from MV2 import *


def run(user, balance, behavior_probability):
    s = supplier.Trader(user=user,
                        balance=float(balance),
                        behavior_probability=float(behavior_probability))


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="supplier")

    parser.add_argument("-u",
                        "--user",
                        help="user",
                        default="s1")

    parser.add_argument("-ba",
                        "--balance",
                        help="balance",
                        default="100")

    parser.add_argument("-p",
                        "--behavior_probability",
                        help="behavior probability",
                        default="0.5")

    args = parser.parse_args()

    run(user=args.user,
        balance=args.balance,
        behavior_probability=args.behavior_probability)
