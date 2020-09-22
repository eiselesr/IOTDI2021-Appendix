FROM python:3.8

RUN apt-get update \
    && apt-get install -y \
        libopencv-dev

RUN pip3 install opencv-python

WORKDIR "/"

COPY cfg ./cfg
COPY data ./data

COPY  ConsumerBase.py yolov3.weights libdarknet.so  ./

COPY  detect.py yolo_sort.py ./



CMD ["python3", "./detect.py"]
#CMD ["/bin/bash"]