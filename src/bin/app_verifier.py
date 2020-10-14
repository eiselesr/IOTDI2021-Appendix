import os
import time
import argparse
from MV2 import *


def run(user):
    v = verifier.Verifier(user=user)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="verifier")

    parser.add_argument("-u",
                        "--user",
                        help="tenant",
                        default='v1')

    args = parser.parse_args()
    run(user=args.user)