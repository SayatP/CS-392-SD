from confluent_kafka import Consumer


conf = {'bootstrap.servers': "kafka:9092",
        'group.id': "foo",
        'auto.offset.reset': 'smallest'}

c = Consumer(conf)

c.subscribe(['orders'])

print(c.poll())
