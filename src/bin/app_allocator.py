import time
import argparse
from MV2 import *


def run(balance):
    a = allocator.Allocator(balance=float(balance))


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="allocator")

    parser.add_argument("-b",
                        "--balance",
                        help="balance",
                        default="100")

    args = parser.parse_args()

    run(balance=args.balance)
