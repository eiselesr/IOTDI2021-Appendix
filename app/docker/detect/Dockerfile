FROM python:3.8

RUN apt-get update \
    && apt-get install -y \
        libopencv-dev

RUN pip3 install opencv-python

COPY  detect.py yolo_sort.py ConsumerBase.py yolov3.weights libdarknet.so  ./
COPY cfg ./cfg
COPY data ./data

WORKDIR "/"
CMD ["python3", "./detect.py"]
#CMD ["/bin/bash"]