from flask import Blueprint, jsonify

expense_bp = Blueprint("expenses", __name__)


@expense_bp.route("/expenses")
def expenses():
    return jsonify({
        "module": "Expenses",
        "message": "Expense list endpoint"
    })
