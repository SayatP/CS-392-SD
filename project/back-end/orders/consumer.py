from confluent_kafka import Consumer
from json import loads
from time import sleep

conf = {'bootstrap.servers': "kafka:9092",
        'group.id': "orders-processor",
        'auto.offset.reset': 'smallest'}

c = Consumer(conf)

c.subscribe(['orders'])

while True:
    print("###################")
    msg = c.poll()
    print(msg)
    print(msg.value())
