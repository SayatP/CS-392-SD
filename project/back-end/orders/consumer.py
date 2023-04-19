import json
from kafka import KafkaConsumer
from time import sleep

from lib import order_processor

consumer = KafkaConsumer(
    'orders',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='order-processor',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    api_version=(0, 10, 1)
)

for event in consumer:
    order_processor.process(event.value)
    print(event.value)
