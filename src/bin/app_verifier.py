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


    args = parser.parse_args()

    s = verifier.Verifier(tenant=args.tenant)
    time.sleep(5)

    while True:
        time.sleep(0.1)