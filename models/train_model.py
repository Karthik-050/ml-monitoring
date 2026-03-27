import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# ---------------- LOAD DATA ----------------
data = pd.read_csv("student_behavior_dataset.csv")

# Clean data
data = data.dropna()

# ---------------- FEATURES ----------------
features = [
    "typing_time",
    "paste_events",
    "paste_length",
    "avg_typing_speed",
    "tab_switches",
    "time_to_code_ratio"
]

X = data[features]

# ---------------- TRAIN MODEL ----------------
model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42
)

model.fit(X)

# ---------------- 🔥 ADD THIS PART ----------------
predictions = model.predict(X)

print("Total Normal:", sum(predictions == 1))
print("Total Suspicious:", sum(predictions == -1))

# ---------------- SAVE MODEL ----------------
joblib.dump(model, "models/isolation_model.pkl")

print("✅ Model trained and saved successfully!")