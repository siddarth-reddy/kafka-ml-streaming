# Real-Time Bike Sharing Streaming with Apache Kafka and Faust
**ENGR 5785G — Assignment 1**

## Overview
This project builds a real-time ML inference pipeline using Apache Kafka and Faust Streams. Rows from the UCI Bike Sharing dataset are streamed through Kafka at ~1 row/second, processed by a pre-trained Random Forest model, and predictions are printed live to a consumer terminal.

## Dataset
**UCI Bike Sharing Dataset (hour.csv)**

| Property | Details |
|----------|---------|
| Source | archive.ics.uci.edu/dataset/275 |
| Records | 17,379 hourly measurements |
| Period | January 2011 – December 2012 |
| ML Task | Regression — predict hourly bike rental count (cnt) |
| Features Used | temp, hum, windspeed, hr, season, weathersit |

## Streams Library
**Python + Faust (faust-streaming)**

The processor uses Faust's @app.agent decorator to define a proper streams topology:

raw-data topic → Faust Agent → Random Forest inference → predictions topic

This is **not** a plain consumer loop — Faust handles the consumer group, offset management, and async stream processing internally.

## ML Model

| Property | Value |
|----------|-------|
| Algorithm | Random Forest Regressor |
| Trees | 100 |
| Target | cnt (hourly bike rental count) |
| MAE | 65.76 |
| R² | 0.679 |

The model is trained offline (train_model.py) and loaded once at Faust processor startup. Every incoming record is fed to the model and the prediction is published to the predictions topic.

## Architecture

producer.py → [raw-data topic] → app.py (Faust @app.agent) → [predictions topic] → consumer.py

| Component | File | Role |
|-----------|------|------|
| Producer | producer.py | Reads hour.csv row by row, publishes each as JSON to raw-data topic at 1 row/second |
| Streams Processor | app.py | Faust agent consumes raw-data, runs Random Forest model, publishes result to predictions topic |
| Output Consumer | consumer.py | Reads from predictions topic and prints each prediction live to the console |

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/your-username/kafka-bike.git
cd kafka-bike
```

### 2. Install Python dependencies
```bash
py -3.11 -m pip install faust-streaming scikit-learn pandas confluent-kafka joblib aiokafka==0.11.0
```

### 3. Configure Confluent Cloud
Create a free cluster at confluent.io and create two topics: raw-data and predictions. Update credentials in each .py file:
```bash
BOOTSTRAP_SERVER = "your-bootstrap-server:9092"
API_KEY = "your-api-key"
API_SECRET = "your-api-secret"
```

### 4. Train the model (one-time)
```bash
py -3.11 train_model.py
```
This saves model.pkl in the project folder.

## Running the Pipeline

Open three terminals side by side and run in this order:

### Terminal 1 — Faust Streams Processor (start first)
```bash
py -3.11 -m faust -A app worker -l info
```
Wait until you see Ready before proceeding.

### Terminal 2 — Producer
```bash
py -3.11 producer.py
```

### Terminal 3 — Output Consumer
```bash
py -3.11 consumer.py
```

Wait 5–10 seconds for Faust to initialize, then start the producer. Predictions will appear in Terminal 3 in real time.

## Project Structure

```
kafka-bike/
├── producer.py           # Reads CSV → publishes to raw-data topic
├── app.py                # Faust agent: raw-data → ML predict → predictions topic
├── consumer.py           # Reads predictions topic → prints to console
├── train_model.py        # Offline training script (run once)
├── hour.csv              # UCI Bike Sharing dataset
├── requirements.txt      # Python dependencies
└── README.md
```

## Video Demo
https://drive.google.com/file/d/1jn6IhnOVWhBSVqQogWFHluExn13c7Ua9/view?usp=sharing

