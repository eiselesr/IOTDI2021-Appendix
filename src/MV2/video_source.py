import os
import pulsar


frame_loc = "/home/ubuntu/projects/MODiCuM-Streaming/frames/"


client = pulsar.Client('pulsar://localhost:6650')


producer = client.create_producer(
    topic='input',
    schema=pulsar.schema.BytesSchema())

for frame_num, file in enumerate(os.listdir(frame_loc)):

    # file_name = str.encode(file)
    with open(frame_loc+file, 'rb') as imageFile:
        frame = bytes(bytearray(imageFile.read()))
        # print(frame)
        # print(type(frame))
        producer.send(frame)
        # print(frame_num)
        if frame_num == 3:
            break
