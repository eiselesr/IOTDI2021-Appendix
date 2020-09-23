FROM ubuntu:20.04
WORKDIR /app
COPY . .
RUN apt-get update && \
  apt-get install -y software-properties-common && \
  add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y python3
RUN apt install -y python3-pip
RUN pip3 install pulsar-client==2.6.1
RUN apt-get -y remove docker docker-engine docker.io containerd runc
RUN apt-get -y update
RUN apt-get -y install \
  apt-transport-https \
  ca-certificates \
  curl \
  gnupg-agent \
  software-properties-common
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
RUN add-apt-repository \
  "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) \
  stable"
RUN apt-get -y update
RUN apt-get -y install docker-ce docker-ce-cli containerd.io