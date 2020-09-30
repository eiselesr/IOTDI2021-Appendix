FROM python:3.8.5
COPY . /code
WORKDIR /code
RUN pip install -r /requirements.txt
WORKDIR /code/bin
ENTRYPOINT ["python", "allocator.py"]