from confluent_kafka import Consumer
import json

BOOTSTRAP_SERVER = "pkc-921jm.us-east-2.aws.confluent.cloud:9092"
API_KEY = "76LRRY74VUAK47IZ"
API_SECRET = "cflt75cSr/ta+P5hLGU7X8WzzgPHq52ACHhsjVD3ezhLRDpXh9c4r/BAY1LgCuMQ"

conf = {
    'bootstrap.servers': BOOTSTRAP_SERVER,
    'sasl.mechanisms': 'PLAIN',
    'security.protocol': 'SASL_SSL',
    'sasl.username': API_KEY,
    'sasl.password': API_SECRET,
    'group.id': 'output-consumer',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(["predictions"])

print("Starting consumer... waiting for predictions")

while True:
    msg = consumer.poll(1.0)
    if msg and not msg.error():
        result = json.loads(msg.value())
        print(f"PREDICTION: {result['prediction']} | INPUT: {result['input']}")