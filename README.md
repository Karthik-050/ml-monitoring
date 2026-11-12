# ML-Based Exam Monitoring and Plagiarism Detection

A Flask application for online programming exams. It runs submitted Python code against a fixed test output, records selected student activity, compares submissions using text similarity, and provides a faculty dashboard.

The system produces indicators for review. An anomaly, paste event, or similarity score is not proof of cheating.

## Features in the repository



- **Programming exam page** with an editor and browser-side tracking for paste events, pasted character count, typing time, typing speed, and tab visibility changes.
- **Python code runner** exposed through Flask at `/api/run`.
- **Submission logging** to MongoDB, including code, selected behavior metrics, risk level, and timestamp.
- **Isolation Forest training script** using a student behavior CSV dataset.
- **TF-IDF cosine similarity** between a submitted program and previously stored submissions.
- **Faculty dashboard** with summary counts and per-student submission history.
- **Admin login endpoint** that issues a JWT.

## Technology

- Python
- Flask
- MongoDB with PyMongo
- scikit-learn
- pandas
- joblib
- JavaScript, HTML, and CSS

## Project structure

```text
.
├── app.py
├── compile/
│   └── compile.py
├── data/
│   └── student_behavior_dataset.csv
├── db/
│   └── db.py
├── models/
│   ├── isolation_model.pkl
│   ├── student_behavior_dataset.csv
│   └── train_model.py
├── routes/
│   ├── auth.py
│   ├── logs.py
│   └── report.py
├── templates/
│   ├── dashboard.html
│   └── exam.html
├── utils/
│   └── similarity.py
├── student_behavior_dataset.csv
└── train2.py
```

## Requirements

Install the Python packages used by the application:

```bash
pip install Flask pymongo scikit-learn pandas joblib numpy PyJWT
```

You also need:

- Python installed and available as `python`.
- MongoDB running locally at `mongodb://localhost:27017/`.
- The saved model at `models/isolation_model.pkl`.

## Run the application

From the project root:

```bash
python app.py
```

Flask starts in debug mode using the settings in `app.py`. Open these pages in a browser:

- Exam page: `http://127.0.0.1:5000/exam`
- Faculty dashboard: `http://127.0.0.1:5000/dashboard`

The dashboard obtains data from the API routes. The frontend currently attempts to log in with demo credentials when the page loads.

## API routes

### `POST /api/run`

Runs submitted Python code and passes the submission to the monitoring logic.

Example request:

```json
{
  "student_id": 101,
  "problem_id": 1,
  "code": "print('1 2 3 5 8')",
  "paste_events": 0,
  "paste_length": 0,
  "typing_time": 30,
  "avg_typing_speed": 2.1,
  "tab_switches": 0
}
```

The runner currently compares output against a fixed expected string for the Bubble Sort exercise:

```text
1 2 3 5 8
```

It returns a compilation/run status and program output. The submission monitoring result is saved by the backend but is not currently included in the `/api/run` response.

### `POST /api/logs`

Processes and stores a submission directly through the logging route. The route expects JSON with a `student_id` and can accept code and behavior fields.

### `POST /api/admin/login`

Accepts the demo admin username and password and returns a JWT on success.

### `GET /api/report/all`

Returns submission totals and a student-level summary.

### `GET /api/report/student/<student_id>`

Returns a student’s submission history.

## Machine learning

`models/train_model.py` trains an Isolation Forest using these six features:

- `typing_time`
- `paste_events`
- `paste_length`
- `avg_typing_speed`
- `tab_switches`
- `time_to_code_ratio`

The script saves the trained model to `models/isolation_model.pkl`. Isolation Forest predictions use `1` for inlier and `-1` for anomaly.

The current inference code needs alignment with the training features: the logging route currently sends seven values in a different order. Until that is corrected, treat the ML result as unverified.

The provided behavior dataset appears to be generated for development. Results on synthetic data do not establish real-world cheating detection accuracy.

## Code similarity

`utils/similarity.py` removes whitespace and uses TF-IDF cosine similarity to compare code strings. The logging route compares a new submission against stored submissions and flags matches above its current threshold.

This is a basic text similarity approach. It does not perform AST-based comparison, and common code patterns may affect similarity results.

## Current limitations

- The exam page submits to `/api/run`; some collected metrics do not reach the monitoring logic.
- The compile route sets multiple behavior features to zero when calling submission processing.
- The model training and inference feature counts and ordering do not match.
- The code runner uses a fixed expected output for one problem.
- Similarity results are text-based and should be reviewed by a person.
- MongoDB logging requires a running local MongoDB instance.
- Dashboard report routes do not enforce authentication in the visible implementation.
- The admin credentials and JWT secret are hardcoded demo values and should be replaced before deployment.
- Running submitted Python code with `subprocess` is unsafe for an untrusted or public-facing service. Use a properly isolated execution environment before exposing the runner beyond a controlled local demo.

## Responsible use

Use monitoring results as evidence for human review, not as an automatic determination of misconduct. Behavior such as pasting, typing quickly, or switching tabs can have legitimate explanations. Provide clear notice to students about what activity is collected and how it is used.
