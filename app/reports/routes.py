from flask import Blueprint, jsonify

report_bp = Blueprint("reports", __name__)


@report_bp.route("/reports")
def reports():
    return jsonify({
        "module": "Reports",
        "message": "Reports endpoint"
    })
