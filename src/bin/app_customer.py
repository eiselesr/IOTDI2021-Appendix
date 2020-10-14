import time
import argparse
import uuid
from MV2 import *


def run(jobid,
        start,
        end,
        service_name,
        user,
        replicas):
    c = customer.Trader(jobid=jobid,
                        start=start,
                        end=end,
                        service_name=service_name,
                        user=user,
                        replicas=int(replicas))


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="customer")

    parser.add_argument("-i",
                        "--jobid",
                        help="jobid",
                        default="none")

    parser.add_argument("-s",
                        "--start",
                        help="start time",
                        default="none")

    parser.add_argument("-e",
                        "--end",
                        help="end time",
                        default="none")

    parser.add_argument("-sn",
                        "--service_name",
                        help="service name",
                        default="rand_nums")

    parser.add_argument("-u",
                        "--user",
                        help="tenant",
                        default="c1")

    parser.add_argument("-r",
                        "--replicas",
                        help="number of replicas",
                        default="2")

    args = parser.parse_args()

    if args.start=="none":
        start = time.time() + 30
    else:
        start = float(args.start)

    if args.end=="none":
        end = start + 600
    else:
        end = float(args.end)

    if args.jobid=="none":
        jobid = str(uuid.uuid4())
    else:
        jobid = args.jobid

    run(jobid=jobid,
        start=start,
        end=end,
        service_name=args.service_name,
        user=args.user,
        replicas=args.replicas)

