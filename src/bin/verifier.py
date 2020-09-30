import os
os.chdir(os.path.join(os.getcwd(), "MV2"))
import verifier
import time
import argparse


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="verifier")

    parser.add_argument("-t",
                        "--tenant",
                        help="tenant",
                        default='sh4')
    args = parser.parse_args()

    v = verifier.Verifier(tenant=args.tenant)

    while True:
        time.sleep(1)