from flask import Blueprint, request, jsonify
import joblib
import numpy as np
from utils.similarity import calculate_similarity
from db.db import collection
from datetime import datetime
from utils.similarity import calculate_similarity, clean_code

logs_bp = Blueprint("logs", __name__)

model = joblib.load("models/isolation_model.pkl")


def process_submission(data):

    # ---------------- CLEAN DATA ----------------
    student_id = int(data["student_id"])
    code = data.get("code", "")

    # ---------------- DEFAULT VALUES ----------------
    risk = "Normal"
    reason = "Behavior within normal range"
    matched_student = None
    similarity_percent = None

    invalid_code = False

    code_length = len(code.strip())
    line_count = len(code.strip().split("\n"))

    if code_length < 20 or line_count < 2:
        risk = "Low"
        reason = "Incomplete or very short code"
        invalid_code = True
    
    
        
    # ---------------- RULE 1: COPY-PASTE ----------------
    if not invalid_code  and data.get("paste_events", 0) > 0:
        risk = "High"
        reason = "Copy-Paste detected"

    else:

        # ---------------- RULE 2: SIMILARITY ----------------
        if not invalid_code:
            previous_submissions = collection.find({})
    
            for submission in previous_submissions:

            # 🔥 FIX: skip same student properly
                try:
                    if int(submission.get("student_id")) == student_id:
                        continue
                except:
                    continue

                similarity = calculate_similarity(clean_code(code), clean_code(submission.get("code", "")))

                if similarity > 0.9:

                    matched_student = submission.get("student_id")
                    similarity_percent = round(similarity * 100, 2)

                    risk = "High"
                    reason = f"Copied from Student {matched_student} ({similarity_percent}%)"

                    break

        # ---------------- RULE 3: ML ----------------
        if not invalid_code and risk == "Normal" and data.get("typing_time", 0) > 0:

            feature_vector = np.array([[

                data.get("typing_time", 0),
                data.get("paste_events", 0),
                data.get("paste_length", 0),
                data.get("attempts", 1),
                data.get("similarity_score", 0),
                data.get("avg_typing_speed", 0),
                data.get("time_to_code_ratio", 0)

            ]])

            prediction = model.predict(feature_vector)

            if prediction[0] == -1 and code_length > 30:
                if risk == "Normal":   # only if no other issue
                     risk = "Medium"
                     reason = "Unusual behavior detected"

    # ---------------- STORE IN DB ----------------
    document = {

        "student_id": student_id,
        "problem_id": data.get("problem_id", 1),

        "typing_time": data.get("typing_time", 0),
        "paste_events": data.get("paste_events", 0),
        "paste_length": data.get("paste_length", 0),
        "attempts": data.get("attempts", 1),
        "similarity_score": data.get("similarity_score", 0),
        "avg_typing_speed": data.get("avg_typing_speed", 0),
        "time_to_code_ratio": data.get("time_to_code_ratio", 0),

        "code": code,

        "risk_level": risk,
        "reason": reason,
        "matched_with": matched_student,
        "similarity_percent": similarity_percent,

        "created_at": datetime.utcnow()

    }

    collection.insert_one(document)

    return {

        "risk_level": risk,
        "reason": reason,
        "matched_with": matched_student,
        "similarity_percent": similarity_percent

    }


# ---------------- API ----------------
@logs_bp.route("/api/logs", methods=["POST"])
def collect_logs():

    data = request.get_json()
    
    print("Incoming data:", data)
    
    result = process_submission(data)

    return jsonify({
        "status": "success",
        **result
    }), 200