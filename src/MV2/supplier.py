import PulsarREST

if __name__ == "__main__":

    tenant = "public"
    namespace = "default"
    className = "ReadInput"
    functionName = "ReadInput"

    api_url = f"http://localhost:8080/admin/v3/functions/{tenant}/{namespace}/{functionName}"
    function_path = f"/home/ubuntu/projects/MODiCuM-Streaming/src/MV2/PulsarFunctions/{functionName}.py"

    config = {"tenant": f"{tenant}",
              "namespace": f"{namespace}",
              "name": functionName,
              "className": f"{className}.{functionName}",
              "inputs": [f"persistent://{tenant}/{namespace}/input"],
              "output": f"persistent://{tenant}/{namespace}/output",
              "outputSchemaType": "",
              "forwardSourceMessageProperty": True,
              "userConfig": {},
              "py": function_path}

    print(config)


    PulsarREST.create_function(api_url, config, function_path)

    PulsarREST.get_functions()