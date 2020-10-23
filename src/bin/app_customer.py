import time
import argparse
import uuid
from MV2 import *


def run(user,
        balance,
        replicas,
        behavior_probability,
        num_jobs,
        namespace=None,
        simnum=None,
        supplierprob=None):
    c = customer.Trader(user=user,
                        balance=float(balance),
                        replicas=int(replicas),
                        behavior_probability=float(behavior_probability),
                        num_jobs=int(num_jobs),
                        namespace=namespace,
                        simnum=simnum,
                        supplierprob=supplierprob)


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
        args.replicas,
        args.behavior_probability,
        args.num_jobs)

