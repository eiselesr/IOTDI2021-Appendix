import os
import time
import argparse
from MV2 import *


def run(user):
    m = mediator.Mediator(user=user)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="mediator")

    parser.add_argument("-u",
                        "--user",
                        help="tenant",
                        default='m1')

    args = parser.parse_args()
    run(user=args.user)