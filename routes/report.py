from flask import Blueprint, jsonify, request
from db.db import collection
from collections import defaultdict

report_bp = Blueprint("report", __name__)


# ------------------------------
# MAIN DASHBOARD (GROUPED)
# ------------------------------
@report_bp.route("/api/report/all", methods=["GET"])
def get_all_report():

    submissions = list(collection.find())

    grouped = defaultdict(list)

    # group by student_id
    for s in submissions:
        grouped[s["student_id"]].append(s)

    students = []

    total = len(submissions)
    high_count = 0
    normal_count = 0

    for student_id, records in grouped.items():

        attempts = len(records)

        high_flag = False

        for r in records:
            if r.get("risk_level") == "High":
                high_flag = True
                break

        if high_flag:
            high_count += 1
        else:
            normal_count += 1

        students.append({
            "student_id": student_id,
            "attempts": attempts,
            "risk_level": "High" if high_flag else "Normal"
        })

    return jsonify({
        "status": "success",
        "total_submissions": total,
        "high_risk_count": high_count,
        "normal_count": normal_count,
        "students": students
    })


# ------------------------------
# STUDENT HISTORY (DETAIL VIEW)
# ------------------------------
@report_bp.route("/api/report/student/<int:student_id>", methods=["GET"])
def student_history(student_id):

    records = list(collection.find({
    "$or": [
        {"student_id": student_id},
        {"student_id": str(student_id)}
    ]
}))

    history = []

    for i, r in enumerate(records):

        history.append({
            "attempt": i + 1,
            "paste_events": r.get("paste_events", 0),
            "risk_level": r.get("risk_level"),
            "reason": r.get("reason")
        })

    return jsonify({
        "student_id": student_id,
        "history": history
    })