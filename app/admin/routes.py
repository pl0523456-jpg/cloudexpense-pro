from flask import Blueprint, jsonify
from flask_login import current_user, login_required

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin")
@login_required
def admin():
    if current_user.role != "admin":
        return jsonify({
            "error": "Forbidden",
            "message": "Admin access required"
        }), 403

    return jsonify({
        "module": "Administration",
        "message": "Admin endpoint"
    })
