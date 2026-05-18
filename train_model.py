import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# Load dataset
df = pd.read_csv("hour.csv")

# Features and target
features = ["temp", "hum", "windspeed", "hr", "season", "weathersit"]
target = "cnt"

X = df[features]
y = df[target]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
preds = model.predict(X_test)
print("MAE:", round(mean_absolute_error(y_test, preds), 2))
print("R2 Score:", round(r2_score(y_test, preds), 3))

# Save model
joblib.dump(model, "model.pkl")
print("Model saved as model.pkl")