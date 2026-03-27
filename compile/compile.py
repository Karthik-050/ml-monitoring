from flask import Blueprint, request, jsonify
import subprocess
import tempfile
import os

from routes.logs import process_submission

compile_bp = Blueprint("compile", __name__)


# ---------------- NORMALIZE FUNCTION ----------------
def normalize(s):
    return " ".join(s.strip().split())


# ---------------- RUN CODE ----------------
@compile_bp.route("/api/run", methods=["POST"])
def run_code():

    data = request.get_json()

    student_id = data.get("student_id")
    problem_id = 1   # only one problem

    code = data.get("code", "")

    paste_events = data.get("paste_events", 0)
    paste_length = data.get("paste_length", 0)

    if not code.strip():
        return jsonify({
            "status": "ERROR",
            "output": "No code submitted"
        })

    # ---------------- TEST CASE ----------------
    expected_output = "1 2 3 5 8"

    # ---------------- EXECUTE CODE ----------------
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as f:
        f.write(code.encode())
        filename = f.name

    try:

        result = subprocess.run(
            ["python", filename],
            text=True,
            capture_output=True,
            timeout=5
        )

        output = result.stdout

        # ✅ FIXED COMPARISON
        if normalize(output) == normalize(expected_output):
            status = "PASS"
        else:
            status = "FAIL"

    except Exception as e:
        output = str(e)
        status = "ERROR"

    finally:
        os.remove(filename)

    # ---------------- ML PROCESS ----------------
    ml_result = process_submission({

        "student_id": int(student_id),
        "problem_id": problem_id,

        "typing_time": 0,
        "paste_events": paste_events,
        "paste_length": paste_length,
        "attempts": 1,
        "similarity_score": 0,
        "avg_typing_speed": 0,
        "time_to_code_ratio": 0,

        "code": code

    })

    # ---------------- RESPONSE ----------------
    return jsonify({

        "status": status,
        "output": output,

       

    })