import pandas as pd
import random

data = []

# ---------------- NORMAL STUDENTS ----------------
for _ in range(700):

    typing_time = random.randint(90, 200)
    paste_events = random.randint(0, 1)
    paste_length = paste_events * random.randint(0, 20)

    avg_typing_speed = round(random.uniform(1.8, 3.5), 2)
    tab_switches = random.randint(0, 1)
    time_to_code_ratio = round(random.uniform(0.6, 1.0), 2)

    label = 0  # normal

    data.append([
        typing_time,
        paste_events,
        paste_length,
        avg_typing_speed,
        tab_switches,
        time_to_code_ratio,
        label
    ])


# ---------------- SUSPICIOUS STUDENTS ----------------
for _ in range(300):

    typing_time = random.randint(50, 120)
    paste_events = random.randint(3, 10)
    paste_length = paste_events * random.randint(50, 200)

    avg_typing_speed = round(random.uniform(0.5, 1.5), 2)
    tab_switches = random.randint(3, 8)
    time_to_code_ratio = round(random.uniform(0.3, 0.7), 2)

    label = 1  # suspicious

    data.append([
        typing_time,
        paste_events,
        paste_length,
        avg_typing_speed,
        tab_switches,
        time_to_code_ratio,
        label
    ])


# ---------------- CREATE DATAFRAME ----------------

df = pd.DataFrame(data, columns=[
    "typing_time",
    "paste_events",
    "paste_length",
    "avg_typing_speed",
    "tab_switches",
    "time_to_code_ratio",
    "label"
])

# Shuffle dataset
df = df.sample(frac=1).reset_index(drop=True)

# Save
df.to_csv("student_behavior_dataset.csv", index=False)

print("Dataset created successfully!")