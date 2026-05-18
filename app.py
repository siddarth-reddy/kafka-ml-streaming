import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())
import faust
import json
import joblib
import ssl


BOOTSTRAP_SERVER = "pkc-921jm.us-east-2.aws.confluent.cloud:9092"
API_KEY = "76LRRY74VUAK47IZ"
API_SECRET = "cflt75cSr/ta+P5hLGU7X8WzzgPHq52ACHhsjVD3ezhLRDpXh9c4r/BAY1LgCuMQ"

ssl_context = ssl.create_default_context()

app = faust.App(
    "ml-processor",
    broker=f"kafka://{BOOTSTRAP_SERVER}",
    broker_credentials=faust.SASLCredentials(
        username=API_KEY,
        password=API_SECRET,
        mechanism="PLAIN",
        ssl_context=ssl_context,
    ),
    topic_replication_factor=3,
    topic_partitions=1,
)

raw_topic = app.topic("raw-data", value_type=bytes)
predictions_topic = app.topic("predictions", value_type=bytes)

model = joblib.load("model.pkl")

@app.agent(raw_topic)
async def process(stream):
    async for message in stream:
        if isinstance(message, bytes):
            data = json.loads(message)
        else:
            data = message
        features = [[
            data["temp"],
            data["hum"],
            data["windspeed"],
            data["hr"],
            data["season"],
            data["weathersit"]
        ]]
        prediction = model.predict(features)[0]
        result = {"input": data, "prediction": round(float(prediction), 2)}
        await predictions_topic.send(value=json.dumps(result).encode())
        print(f"[Processor] Prediction: {result['prediction']} for input: {data}")

if __name__ == "__main__":
    app.main()