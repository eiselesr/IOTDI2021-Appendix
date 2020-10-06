import os
os.chdir(os.path.join(os.getcwd(), "MV2"))
import supplier
import time
import argparse


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="supplier")

    parser.add_argument("-t",
                        "--tenant",
                        help="tenant",
                        default='s1')

    parser.add_argument("-e",
                        "--seed",
                        help="seed",
                        default='1')


    args = parser.parse_args()

    s = supplier.Trader(tenant=args.tenant, seed=int(args.seed))

    time.sleep(5)

    while True:
        s.post_offer()
        msg = s.get_allocation()
        s.do_job()