import os
import pulsar

# frame_loc = os.environ['FRAMES']
frame_loc = "/home/ubuntu/projects/MODiCuM-Streaming/frames/"

# # send 10 messages
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
        if frame_num==3:
            break




consumer = client.subscribe(topic='input',
                            subscription_name='frame-input',
                            initial_position=pulsar.InitialPosition.Earliest)
#
count = 0
# while (count <= 10):
while True:
    try:
        msg = consumer.receive(timeout_millis=60000)
        print(type(msg.data()))
        with open('frameFile.jpg', 'wb') as tmp:
            tmp.write(msg.data())

        # print(type(msg))
        consumer.acknowledge(msg)
        count += 1
    except:
        print("Test failed: timeout received {} messages of 10 total messages".format(count))
        client.close()
        quit()
#
# print("Test succeeded")
client.close()