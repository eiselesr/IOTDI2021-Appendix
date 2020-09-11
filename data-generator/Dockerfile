FROM ubuntu:20.04
WORKDIR /app
COPY . .
RUN apt-get update && \
  apt-get install -y software-properties-common && \
  add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y python3
RUN apt install -y python3-pip
RUN pip3 install pulsar-client==2.6.1