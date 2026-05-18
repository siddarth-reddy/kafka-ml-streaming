# Real-Time Streaming ML Pipeline with Apache Kafka and Faust

## Dataset
I used the **Bike Sharing Dataset (UCI)** (`hour.csv`), which contains hourly bike rental counts along with weather and time features. I chose this dataset because it has clear numeric features that work well for regression, and it simulates a real-world streaming scenario where sensor data arrives continuously.

## Streaming Library
I used **Faust** (faust-streaming), a Python stream processing library built on top of Apache Kafka. It acts as the Kafka Streams equivalent for Python, allowing me to build real-time agents that consume, process, and produce Kafka messages.

## Architecture
hour.csv → producer.py → [raw-data topic] → app.py (Faust) → [predictions topic] → consumer.py

## ML Model
- Model: Random Forest Regressor (scikit-learn)
- Features: temp, hum, windspeed, hr, season, weathersit
- Target: cnt (hourly bike rental count)
- MAE: 65.76
- R2 Score: 0.679

## Setup Instructions

Install dependencies:
py -3.11 -m pip install faust-streaming scikit-learn pandas confluent-kafka joblib
py -3.11 -m pip install aiokafka==0.11.0

Train the model:
py -3.11 train_model.py

## How to Run

Open 3 terminals in this order:

Terminal 1 - Start Faust processor:
py -3.11 -m faust -A app worker -l info

Terminal 2 - Start Producer (wait 10 seconds after Terminal 1):
py -3.11 producer.py

Terminal 3 - Start Consumer:
py -3.11 consumer.py

## Demo Video
[Link to demo video]