from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from app.models.expense import Expense


report_bp = Blueprint("reports", __name__)


@report_bp.route("/reports", methods=["GET"])
@login_required
def reports():

    user_expenses = Expense.query.filter_by(
        user_id=current_user.id
    ).all()

    total_expenses = sum(
        float(expense.amount)
        for expense in user_expenses
    )

    expense_count = len(user_expenses)

    average_expense = (
        total_expenses / expense_count
        if expense_count > 0
        else 0
    )

    category_totals = {}

    for expense in user_expenses:
        category = expense.category

        category_totals[category] = (
            category_totals.get(category, 0)
            + float(expense.amount)
        )

    return jsonify({
        "report": {
            "user_id": current_user.id,
            "expense_count": expense_count,
            "total_expenses": total_expenses,
            "average_expense": average_expense,
            "category_totals": category_totals
        }
    }), 200
