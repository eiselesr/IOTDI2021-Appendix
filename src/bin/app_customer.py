import time
import argparse
from MV2 import *


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="customer")

    parser.add_argument("-t",
                        "--tenant",
                        help="tenant")

    parser.add_argument("-r",
                        "--replicas",
                        help="number of replicas")

    parser.add_argument("-a",
                        "--service_name",
                        help="name of service")

    parser.add_argument("-st",
                        "--start_time",
                        help="start time in seconds",
                        default="none")

    parser.add_argument("-et",
                        "--end_time",
                        help="end time in seconds",
                        default="none")


    args = parser.parse_args()

    if args.start_time=="none":
        start_time = time.time()
    else:
        start_time = float(args.start_time)

    if args.end_time=="none":
        end_time = time.time() + 600
    else:
        end_time = float(args.end_time)

    c = customer.Trader(tenant=args.tenant,
                        replicas=int(args.replicas),
                        service_name=args.service_name,
                        start_time=start_time,
                        end_time=end_time)

    c.run()
    c.close()
