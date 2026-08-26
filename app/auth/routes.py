from flask import Blueprint, request, jsonify
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from app.extensions import db
from app.models.user import User


auth_bp = Blueprint("auth", __name__)


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return jsonify({
            "module": "Authentication",
            "message": "Login endpoint",
            "method": "POST"
        }), 200

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must contain JSON"
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "error": "Email and password are required"
        }), 400

    email = email.strip().lower()

    user = db.session.execute(
        db.select(User).where(User.email == email)
    ).scalar_one_or_none()

    if user is None or not user.check_password(password):
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    login_user(user)

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role": user.role
        }
    }), 200


# --------------------------------------------------
# LOGOUT
# --------------------------------------------------

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()

    return jsonify({
        "message": "Logout successful"
    }), 200


# --------------------------------------------------
# CURRENT USER
# --------------------------------------------------

@auth_bp.route("/me", methods=["GET"])
@login_required
def me():
    return jsonify({
        "authenticated": True,
        "user": {
            "id": current_user.id,
            "first_name": current_user.first_name,
            "last_name": current_user.last_name,
            "email": current_user.email,
            "role": current_user.role
        }
    }), 200


# --------------------------------------------------
# REGISTRATION
# --------------------------------------------------

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return jsonify({
            "module": "Authentication",
            "message": "Registration endpoint",
            "method": "POST"
        }), 200

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must contain JSON"
        }), 400

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")

    if not first_name or not last_name or not email or not password:
        return jsonify({
            "error": "First name, last name, email, and password are required"
        }), 400

    first_name = first_name.strip()
    last_name = last_name.strip()
    email = email.strip().lower()

    if not first_name or not last_name or not email:
        return jsonify({
            "error": "First name, last name, and email cannot be empty"
        }), 400

    if len(password) < 8:
        return jsonify({
            "error": "Password must be at least 8 characters"
        }), 400

    existing_user = db.session.execute(
        db.select(User).where(User.email == email)
    ).scalar_one_or_none()

    if existing_user:
        return jsonify({
            "error": "Email already registered"
        }), 409

    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        role="employee"
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "Registration successful",
        "user": {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role": user.role
        }
    }), 201


# --------------------------------------------------
# PASSWORD RECOVERY
# --------------------------------------------------

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must contain JSON"
        }), 400

    email = data.get("email")

    if not email:
        return jsonify({
            "error": "Email is required"
        }), 400

    email = email.strip().lower()

    user = db.session.execute(
        db.select(User).where(User.email == email)
    ).scalar_one_or_none()

    if user is None:
        return jsonify({
            "error": "Account not found"
        }), 404

    if not user.security_question_1:
        return jsonify({
            "error": "Security questions are not configured"
        }), 400

    return jsonify({
        "message": "Security questions retrieved",
        "questions": [
            user.security_question_1,
            user.security_question_2,
            user.security_question_3
        ]
    }), 200


# --------------------------------------------------
# RESET PASSWORD
# --------------------------------------------------

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must contain JSON"
        }), 400

    email = data.get("email")
    answers = data.get("answers")
    new_password = data.get("new_password")

    if not email or not answers or not new_password:
        return jsonify({
            "error": "Email, answers, and new password are required"
        }), 400

    if not isinstance(answers, list) or len(answers) != 3:
        return jsonify({
            "error": "Exactly 3 security answers are required"
        }), 400

    if len(new_password) < 8:
        return jsonify({
            "error": "New password must be at least 8 characters"
        }), 400

    email = email.strip().lower()

    user = db.session.execute(
        db.select(User).where(User.email == email)
    ).scalar_one_or_none()

    if user is None:
        return jsonify({
            "error": "Invalid recovery information"
        }), 401

    for question_number, answer in enumerate(answers, start=1):
        if not user.check_security_answer(question_number, answer):
            return jsonify({
                "error": "Invalid recovery information"
            }), 401

    user.set_password(new_password)

    db.session.commit()

    return jsonify({
        "message": "Password reset successful"
    }), 200
