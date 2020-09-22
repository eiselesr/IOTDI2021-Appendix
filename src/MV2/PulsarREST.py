import requests
import json
from requests_toolbelt import MultipartEncoder


def get_functions():

    api = "http://localhost:8080/admin/v3/functions/public/default"
    headers = {'Content-Type': "application/json",
               'Accept': "application/json"}
    r = requests.get(api, headers=headers)

    print(r.json())
    print(r.request.url)


def create_reverse():

    api_url = f"http://localhost:8080/admin/v3/functions/public/default/reverse"

    config = {"tenant": "public",
              "namespace": "default",
              "name": "reverse",
              "className": "reverse",
              "inputs": ["persistent://public/default/backwards"],
              "output": "persistent://public/default/forwards",
              "outputSchemaType": "",
              "forwardSourceMessageProperty": True,
              "userConfig": {},
              "py": "/shared/reverse.py"}

    file = open('/home/ubuntu/IdeaProjects/pulsar-python-helloWorld/shared/reverse.py', 'rb')
    mp_encoder = MultipartEncoder(
        fields={
            'functionConfig': (None, json.dumps(config), 'application/json'),
            'data': ("reverse.py", file, 'application/octet-stream')
        }
    )

    headers = {'Content-Type': mp_encoder.content_type, 'user-agent': 'Pulsar-Java-v2.6.1'}

    print(mp_encoder)
    print(mp_encoder.content_type)
    print(api_url)
    print(headers)

    response = requests.post(api_url, data=mp_encoder, headers=headers)

    print(response.reason)
    print(response.content)


def create_function(api_url: str, config: dict, function_path: str):
    """
    :param api_url: f"http://localhost:8080/admin/v3/functions/public/default/reverse"
    :param config: config = {"tenant": "public",
                             "namespace": "default",
                             "name": "reverse",
                             "className": "reverse",
                             "inputs": ["persistent://public/default/backwards"],
                             "output": "persistent://public/default/forwards",
                             "outputSchemaType": "",
                             "forwardSourceMessageProperty": True,
                             "userConfig": {},
                             "py": "/shared/reverse.py"}
                   config = {"tenant": str,
                             "namespace": str,
                             "name": str,
                             "className": str,
                             "inputs": list,
                             "output": str,
                             "outputSchemaType": "",
                             "forwardSourceMessageProperty": bool,
                             "userConfig": dict,
                             "py": str}
    :param function_path: "/home/ubuntu/projects/MODiCuM-Streaming/deployment/shared/reverse.py
    :return:
    """

    file = open(function_path, 'rb')
    mp_encoder = MultipartEncoder(
        fields={
            'functionConfig': (None, json.dumps(config), 'application/json'),
            'data': (f"{config['name']}.py", file, 'application/octet-stream')
        }
    )

    headers = {'Content-Type': mp_encoder.content_type, 'user-agent': 'Pulsar-Java-v2.6.1'}

    print(mp_encoder)
    print(mp_encoder.content_type)
    print(api_url)
    print(headers)

    response = requests.post(api_url, data=mp_encoder, headers=headers)

    print(response.reason)
    print(response.content)


if __name__ == "__main__":

    create_reverse()
