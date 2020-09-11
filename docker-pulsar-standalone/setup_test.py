import pulsar

# send 10 messages
client = pulsar.Client('pulsar://localhost:6650')
producer = client.create_producer('my-topic')

for i in range(10):
    producer.send(("Pulsar Message {}".format(i)).encode('utf-8'))


# receive messages
consumer = client.subscribe('my-topic',
                            subscription_name='my-sub',
                            initial_position=pulsar.InitialPosition.Earliest)

count = 0
while (count <= 10):
    try:
        msg = consumer.receive(timeout_millis=60000)
        print("Received message: '%s'" % msg.data().decode("utf-8"))
        consumer.acknowledge(msg)
        count += 1
    except:
        print("Test failed: timeout received {} messages of 10 total messages".format(count))
        client.close()
        quit()

print("Test succeeded")
client.close()