import PulsarREST
import pulsar

if __name__ == "__main__":

    tenant = "public"
    namespace = "default"
    className = "ReadInput"
    functionName = "ReadInput"

    api_url = f"http://localhost:8080/admin/v3/functions/{tenant}/{namespace}/{functionName}"
    function_path = f"/home/ubuntu/projects/MODiCuM-Streaming/src/MV2/PulsarFunctions/{functionName}.py"

    # inputSpecs = {
    #     "property1": {
    #         "schemaType": "BYTES"
    #     }
    # }

        #      "serdeClassName": "string",
        #      "schemaProperties": {
        #          "property1": "string",
        #          "property2": "string"
        #      },
        #      "receiverQueueSize": 0,
        #      "regexPattern": true
        #  },
        # "receiverQueueSize": 0,
        # "regexPattern": True
        # }

    print(pulsar.schema.BytesSchema())

    config = {"tenant": f"{tenant}",
              "namespace": f"{namespace}",
              "name": functionName,
              "className": f"{className}.{functionName}",
              "inputs": [f"persistent://{tenant}/{namespace}/fubar"],
              "output": f"persistent://{tenant}/{namespace}/frobaz",
              # "outputSchemaType": "BYTES",
              "outputSerdeClassName": f"{className}.BytesSerDe",
              "forwardSourceMessageProperty": True,
              "userConfig": {},
              "py": function_path}

    print(config)

    # PulsarREST.create_function(api_url, config, function_path)
    PulsarREST.update_function(api_url, config, function_path)

    PulsarREST.get_functions()