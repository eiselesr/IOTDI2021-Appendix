import os
import pulsar
import time


frame_loc = "/home/ubuntu/projects/MODiCuM-Streaming/frames/"


client = pulsar.Client('pulsar://localhost:6650')


producer = client.create_producer(
    topic='fubar',
    schema=pulsar.schema.BytesSchema())

for frame_num, file in enumerate(os.listdir(frame_loc)):

    # file_name = str.encode(file)
    with open(frame_loc+file, 'rb') as imageFile:
        frame = bytes(bytearray(imageFile.read()))
        # print(frame)
        # print(type(frame))
        properties = {"content-type": "application/jpg", "frame_num": str(frame_num)}
        timestamp = int(round(time.time() * 1000))
        print(f"time is: {timestamp} and of type {type(timestamp)}")
        producer.send(frame, properties, event_timestamp=int(time.time()))
        # print(frame_num)
        if frame_num == 3:
            break
