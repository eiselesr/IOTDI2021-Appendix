#!/bin/bash
NAME=${PWD##*/}
docker network create my-net

docker run -it --rm --name $NAME --network my-net \
  -p 6650:6650 \
  -p 8080:8080 \
  --mount source=pulsardata,target=/pulsar/data \
  --mount source=pulsarconf,target=/pulsar/conf \
  apachepulsar/pulsar:2.6.1 \
  bin/pulsar standalone