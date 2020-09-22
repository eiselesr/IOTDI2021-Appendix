import pulsar
import json
import requests
from requests_toolbelt import MultipartEncoder
import pprint
# import zmq

# bin/pulsar-admin functions create \
# 	--py /shared/reverse.py \
# 	--classname reverse \
# 	--inputs persistent://public/default/backwards \
# 	--output persistent://public/default/forwards \
# 	--tenant public \
# 	--namespace default \
# 	--name reverse

# payload = {"inputs": persistent://public/default/input-topic,
#     "parallelism": 4,
#     "output": persistent://public/default/output-topic,
#     "log-topic": persistent://public/default/log-topic,
#     "classname": org.example.test.ExclamationFunction
# }



# https://pulsar.apache.org/admin/v3/functions/{tenant}/{namespace}/{functionName}

def getFunctions():

    api = "http://localhost:8080/admin/v2/functions/public/default"
    headers = {'Content-Type': "application/json",
               'Accept': "application/json"}
    r = requests.get(api, headers=headers)

    print(r.json())
    print(r.request.url)

def create_reverse(pulsar_admin_url=None, tenant=None):
    api_url = f"http://localhost:8080/admin/v3/functions/public/default/reverse"

    
    config = {"tenant":"public",
              "namespace":"default",
              "name":"reverse",
              "className":"reverse",
              "inputs":["persistent://public/default/backwards"],
              "output":"persistent://public/default/forwards",
              "outputSchemaType":"",
              "forwardSourceMessageProperty":True,
              "userConfig":{},
              "py":"/shared/reverse.py"}

    file = open('/home/ubuntu/IdeaProjects/pulsar-python-helloWorld/shared/reverse.py', 'rb')
    mp_encoder = MultipartEncoder(
        fields={
            'functionConfig': (None, json.dumps(config), 'application/json'),
            'data': ("reverse.py", file, 'application/octet-stream')
        }
    )

    headers = {'Content-Type': mp_encoder.content_type, 'user-agent': 'Pulsar-Java-v2.6.1'}

    pprint.pprint(mp_encoder)
    print(mp_encoder.content_type)
    print(api_url)
    print(headers)

    response = requests.post(api_url, data=mp_encoder, headers=headers)

    print(response.reason)
    print(response.content)
    print(response)
    # print(response.request.body)



def create_function(pulsar_admin_url=None, tenant=None):
    # create function
    api_url = f"http://localhost:8080/admin/v3/functions/public/default/readInput"


    # mp_encoder = MultipartEncoder(
    #     fields={
    #         'url': 'file://pulsar/lib/org.apache.pulsar-pulsar-functions-api-examples-2.5.1.jar',
    #         'functionConfig': (None, json.dumps({ 'tenant': 'example'}), 'application/json')
    #     }
    # )
    # print(mp_encoder)
    #
    # headers = {'Content-Type': mp_encoder.content_type}
    # response = requests.post(api_url, data=mp_encoder, headers=headers)


    config = {
        "runtime": "PYTHON",
        "inputs": ["persistent://public/default/input"],
        "parallelism": 1,
        "classname": "supplier.readInput",
        "py": "/home/ubuntu/projects/MODiCuM-Streaming/src/MV2/supplier.py",
    }

    # { "inputs": persistent://public/default/input-topic
    #   "parallelism": 4
    #   "output": persistent://public/default/output-topic
    #   "log-topic": persistent://public/default/log-topic
    #   "classname": org.example.test.ExclamationFunction
    #   "jar": java-function-1.0-SNAPSHOT.jar}


    mp_encoder = MultipartEncoder(
        fields={
            'url': 'file://home/ubuntu/projects/MODiCuM-Streaming/src/MV2/supplier.py"',
            'functionConfig': (None, json.dumps(config), 'application/json')
        }
    )

    headers = {'Content-Type': mp_encoder.content_type}

    print(mp_encoder)
    print(mp_encoder.content_type)
    print(api_url)
    print(headers)

    response = requests.post(api_url, data=mp_encoder, headers=headers)




    # payload = {
    #     "inputs": "persistent://public/default/input",
    #     "parallelism": 1,
    #     "classname": "supplier.readInput",
    #     "py": "/home/ubuntu/projects/MODiCuM-Streaming/src/MV2/supplier.py",
    # }
    # # "name": "readInput"
    # # "output": "persistent://public/default/output",
    #
    # payload = json.dumps(payload)
    #
    # headers = {'Content-Type': "multipart/form-data",
    #            'Accept': "application/json"}
    #
    # r = requests.post(url=url, data=payload, headers=headers)

    print(response.reason)
    print(response.request.body)
    # print(response.json())
    # print(response.request.body)
    # print(response.reason)


    # if r.status_code == 200:
    #     print("Pulsar Function successfully created")
    # elif r.status_code == 400:
    #     print("Invalid Request (The Pulsar Function already exists, etc.)")
    # elif r.status_code == 403:
    #     print("The requester doesn't have admin permissions")
    # elif r.status_code == 408:
    #     print("Request timeout")
    # else:
    #     print("unknown error: {}, {}".format(r.status_code, r.content))
    #     quit()



class readInput(pulsar.Function):
    def process(self, input, context):
        # with open('frameFile.jpg', 'wb') as tmp:
        #     tmp.write(input.data())
        print("input: {}".format(input))
        print("type(input): {}".format(type(input)))


if __name__ == "__main__":

    getFunctions()
    # create_function()
    create_reverse()