import time
import argparse
import uuid
from MV2 import *


def run(user,
        balance,
        behavior_probability):
    c = customer.Trader(user=user,
                        balance=float(balance),
                        behavior_probability=float(behavior_probability))


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="customer")

    parser.add_argument("-u",
                        "--user",
                        help="user",
                        default="c1")

    parser.add_argument("-b",
                        "--balance",
                        help="balance",
                        default="100")

    parser.add_argument("-p",
                        "--behavior_probability",
                        help="behavior probability",
                        default="0.5")

    args = parser.parse_args()

    run(args.user,
        args.balance,
        args.behavior_probability)

