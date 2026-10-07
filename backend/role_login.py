# Role-based login endpoint to add to app.py

from flask import jsonify, request
import hashlib
import os


def generate_login_token(role: str, password: str, secret_key: str) -> str:
    """Create a lightweight token so the frontend and API can share a session contract."""
    payload = f"{role}:{password}:{secret_key}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def register_role_login(app, ADMIN_PASSWORD, SECRET_KEY):
    @app.route("/role-login", methods=["POST"])
    def role_login():
        """Validate password for admin, rescue, or government roles."""
        data = request.get_json(silent=True) or {}
        role = data.get("role", "").lower()
        password = data.get("password", "")

        passwords = {
            "admin": ADMIN_PASSWORD,
            "rescue": os.getenv("RESCUE_PASSWORD", "rescue123"),
            "government": os.getenv("GOVERNMENT_PASSWORD", "gov123")
        }

        if role not in passwords:
            return jsonify({"success": False, "message": "Invalid role"}), 400

        if password == passwords[role]:
            return jsonify({
                "success": True,
                "message": f"Welcome {role.title()}",
                "token": generate_login_token(role, password, SECRET_KEY),
            })

        return jsonify({"success": False, "message": "Invalid password"}), 401
