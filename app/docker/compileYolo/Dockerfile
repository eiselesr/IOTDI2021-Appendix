FROM python:3.8

RUN git clone https://github.com/pjreddie/darknet.git

WORKDIR /darknet

RUN make

CMD ["cp", "/darknet/libdarknet.so", "/output"]