import pulsar
import argparse
import requests
import json


def main(pulsar_url,
         tenant,
         namespace,
         topic,
         subscription_name,
         timeout):

    # create consumer
    client = pulsar.Client(pulsar_url)
    full_topic = "persistent://{}/{}/{}".format(tenant, namespace, topic)
    consumer = client.subscribe(full_topic,
                                subscription_name=subscription_name,
                                initial_position=pulsar.InitialPosition.Earliest)
    if timeout == "none":
        timeout = None
    else:
        timeout = int(timeout)
    while True:
        msg = consumer.receive(timeout_millis=timeout)
        print("Received message on topic {}: {}".format(full_topic, msg.data().decode("utf-8")))
        consumer.acknowledge(msg)


def get_args():
    parser = argparse.ArgumentParser(description="data generator")

    parser.add_argument("-p",
                        "--pulsar_url",
                        help="pulsar url",
                        default='pulsar://localhost:6650')

    parser.add_argument("-t",
                        "--tenant",
                        help="pulsar tenant",
                        default='public')

    parser.add_argument("-n",
                        "--namespace",
                        help="pulsar namespace",
                        default='default')

    parser.add_argument("-o",
                        "--topic",
                        help="pulsar topic",
                        default='my-topic')

    parser.add_argument("-r",
                        "--subscription_name",
                        help="name of subscription",
                        default='test-subscription')

    parser.add_argument("-m",
                        "--timeout",
                        help="consumer timeout",
                        default='none')

    return parser.parse_args()


if __name__=="__main__":
    args = get_args()

    main(pulsar_url=args.pulsar_url,
         tenant=args.tenant,
         namespace=args.namespace,
         topic=args.topic,
         subscription_name=args.subscription_name,
         timeout=args.timeout)
