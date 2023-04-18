from confluent_kafka import Consumer

from lib import order_processor

conf = {'bootstrap.servers': "kafka:9092",
        'group.id': "order-processor",
        'auto.offset.reset': 'latest'}

c = Consumer(conf)

c.subscribe(['orders'])

while True:
    msg = c.poll()
    order_processor.process(msg.value())
