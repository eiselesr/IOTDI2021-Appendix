How to build this application

```bash

```

How to run this application

```bash
NAME=${PWD##*/}
docker run -it --rm --name docker-client-1 --network my-net "$NAME:1.0" \
    --pulsar_url "pulsar://docker-pulsar-standalone:6650" \
    --pulsar_admin_url "http://docker-pulsar-standalone:8080/admin/v2" \
    --tenant "newtenant4" \
    --namespace "test2" \
    --topic "test" \
    --message_rate_s 5


python app.py \
    --pulsar_url "pulsar://localhost:6650" \
    --pulsar_admin_url "http://localhost:8080/admin/v2" \
    --tenant "newtenant3" \
    --namespace "test" \
    --topic "test" \
    --message_rate_s 5

#docker run --rm --name docker-client docker-client:1.0
```