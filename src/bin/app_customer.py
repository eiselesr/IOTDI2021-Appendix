import time
import argparse
import uuid
from MV2 import *


def run(user,
        balance,
        b,
        pi_s,
        lam,
        replicas,
        behavior_probability,
        num_jobs):
    c = customer.Trader(user=user,
                        balance=float(balance),
                        b=float(b),
                        pi_s=float(pi_s),
                        lam=float(lam),
                        replicas=int(replicas),
                        behavior_probability=float(behavior_probability),
                        num_jobs=int(num_jobs))


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="customer")

    parser.add_argument("-u",
                        "--user",
                        help="user",
                        default="c1")

    parser.add_argument("-ba",
                        "--balance",
                        help="balance",
                        default="100")

    parser.add_argument("-b",
                        "--b_val",
                        help="benefit",
                        default="100")

    parser.add_argument("-i",
                        "--pi_s",
                        help="supplier cost",
                        default="100")

    parser.add_argument("-l",
                        "--lam",
                        help="lam",
                        default="100")

    parser.add_argument("-r",
                        "--replicas",
                        help="balance",
                        default="2")

    parser.add_argument("-p",
                        "--behavior_probability",
                        help="behavior probability",
                        default="0.5")

    parser.add_argument("-n",
                        "--num_jobs",
                        help="number of jobs to run",
                        default="10")

    args = parser.parse_args()

    run(args.user,
        args.balance,
        args.b_val,
        args.pi_s,
        args.lam,
        args.replicas,
        args.behavior_probability,
        args.num_jobs)

