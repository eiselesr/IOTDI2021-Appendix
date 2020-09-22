import pulsar


class ReadInput(pulsar.Function):
    def __init__(self):
        pass

    def process(self, input, context):
        print("input: {}".format(input))
        print("type(input): {}".format(type(input)))

        topic = context.get_output_topic()

        context.publish(topic, item)

        return input

#
# consumer = client.subscribe(topic='input',
#                             subscription_name='frame-input',
#                             initial_position=pulsar.InitialPosition.Earliest)
# #
# count = 0
# # while (count <= 10):
# while True:
#     try:
#         msg = consumer.receive(timeout_millis=60000)
#         print(type(msg.data()))
#         with open('frameFile.jpg', 'wb') as tmp:
#             tmp.write(msg.data())
#
#         # print(type(msg))
#         consumer.acknowledge(msg)
#         count += 1
#     except:
#         print("Test failed: timeout received {} messages of 10 total messages".format(count))
#         client.close()
#         quit()
# #
# # print("Test succeeded")
# client.close()