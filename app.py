import sys
import os

# Ensure project root is in Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template
from routes.logs import logs_bp
from routes.report import report_bp
from routes.auth import auth_bp
from compile.compile import compile_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(logs_bp)
app.register_blueprint(report_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(compile_bp)


# Faculty Dashboard Route
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# Health check (optional but useful)
@app.route("/")
def home():
    return {
        "status": "running",
        "message": "Exam Monitoring Backend Active"
    }


@app.route("/exam")
def exam():
    return render_template("exam.html")


if __name__ == "__main__":
    app.run(debug=True)