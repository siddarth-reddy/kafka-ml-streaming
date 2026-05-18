import pandas as pd
import json
import time
from confluent_kafka import Producer

# --- YOUR CONFLUENT CLOUD CREDENTIALS ---
BOOTSTRAP_SERVER = "pkc-921jm.us-east-2.aws.confluent.cloud:9092"
API_KEY = "76LRRY74VUAK47IZ"
API_SECRET = "cflt75cSr/ta+P5hLGU7X8WzzgPHq52ACHhsjVD3ezhLRDpXh9c4r/BAY1LgCuMQ"

conf = {
    'bootstrap.servers': BOOTSTRAP_SERVER,
    'sasl.mechanisms': 'PLAIN',
    'security.protocol': 'SASL_SSL',
    'sasl.username': API_KEY,
    'sasl.password': API_SECRET
}

producer = Producer(conf)

# Load dataset
df = pd.read_csv("hour.csv")
features = ["temp", "hum", "windspeed", "hr", "season", "weathersit", "cnt"]
df = df[features]

print("Starting producer... sending 1 row/second")

for i, row in df.iterrows():
    message = row.to_dict()
    producer.produce("raw-data", value=json.dumps(message).encode("utf-8"))
    producer.flush()
    print(f"[Producer] Sent row {i}: {message}")
    time.sleep(1)