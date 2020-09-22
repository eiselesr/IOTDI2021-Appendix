import pulsar
import argparse
import time
import requests
import json

def create_tenant(pulsar_admin_url=None, tenant=None):
    # create tenant
    r = requests.put("{}/tenants/{}".format(pulsar_admin_url, tenant),
                     data=json.dumps({"allowedClusters": ["standalone"]}),
                     headers={'Content-Type': "application/json", 'Accept': "application/json"})

    print(r.request.url)
    print(r.request.body)
    if r.status_code == 409:
        print("tenant already exists")
    elif (r.status_code == 400) or (r.status_code == 204):
        print("new tenant created: {}".format(tenant))
    else:
        print("unknown error: {}, {}".format(r.status_code, r.content))
        quit()


def create_namespace(pulsar_admin_url=None, tenant=None, namespace=None):
    # create tenant
    r = requests.put("{}/namespaces/{}/{}".format(pulsar_admin_url, tenant, namespace))

    if r.status_code == 409:
        print("namespace already exists")
    elif (r.status_code == 400) or (r.status_code == 204):
        print("new namespace created: {}/{}".format(tenant, namespace))
    else:
        print("unknown error: {}, {}".format(r.status_code, r.content))
        quit()

def main(pulsar_url="pulsar://localhost:6650",
         pulsar_admin_url="http://localhost:8080/admin/v2",
         tenant="public",
         namespace="default",
         topic="my-topic",
         message_rate_s=1):

    # create tenant
    create_tenant(pulsar_admin_url=pulsar_admin_url, tenant=tenant)

    # create namespace
    create_namespace(pulsar_admin_url=pulsar_admin_url, tenant=tenant, namespace=namespace)

    # create producer and run application

    client = pulsar.Client(pulsar_url)
    producer = client.create_producer("persistent://{}/{}/{}".format(tenant, namespace, topic))

    i = 0
    while True:
        message = "Pulsar Message number {}".format(i)
        producer.send((message).encode('utf-8'))
        print("Message sent: {}".format(message))
        i += 1
        time.sleep(int(message_rate_s))
    client.close()


def get_args():
    parser = argparse.ArgumentParser(description="data generator")

    parser.add_argument("-p",
                        "--pulsar_url",
                        help="pulsar url",
                        default='pulsar://localhost:6650')

    parser.add_argument("-a",
                        "--pulsar_admin_url",
                        help="pulsar admin rest url",
                        default="http://localhost:8080/admin/v2")

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
                        "--message_rate_s",
                        help="seconds between each message published",
                        default='1')

    args = parser.parse_args()
    return args

if __name__=="__main__":
    args = get_args()

    main(pulsar_url=args.pulsar_url,
         pulsar_admin_url=args.pulsar_admin_url,
         tenant=args.tenant,
         namespace=args.namespace,
         topic=args.topic,
         message_rate_s=args.message_rate_s)
