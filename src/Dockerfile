FROM ubuntu:20.04
RUN apt-get update && \
  apt-get install -y software-properties-common && \
  add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y python3
RUN apt install -y python3-pip
WORKDIR /code
COPY . .
RUN pip3 install -r requirements.txt
