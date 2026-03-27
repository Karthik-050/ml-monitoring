from flask import Blueprint, request, jsonify
import jwt
import datetime

auth_bp = Blueprint("auth", __name__)

SECRET_KEY = "this_is_a_very_long_secure_secret_key_1234567890"

# Hardcoded admin credentials (for demo)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

@auth_bp.route("/api/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json()

    if (data.get("username") == ADMIN_USERNAME and
        data.get("password") == ADMIN_PASSWORD):

        token = jwt.encode({
            "username": ADMIN_USERNAME,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({
            "status": "success",
            "token": token
        }), 200

    return jsonify({
        "status": "error",
        "message": "Invalid credentials"
    }), 401