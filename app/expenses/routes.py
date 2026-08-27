from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from app.extensions import db
from app.models.expense import Expense


expense_bp = Blueprint("expenses", __name__)


# --------------------------------------------------
# EXPENSE LIST / CREATE
# --------------------------------------------------

@expense_bp.route("/expenses", methods=["GET", "POST"])
@login_required
def expenses():

    # ----------------------------------------------
    # CREATE EXPENSE
    # ----------------------------------------------

    if request.method == "POST":
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "error": "Request body must contain JSON"
            }), 400

        title = data.get("title")
        category = data.get("category")
        amount = data.get("amount")
        description = data.get("description")

        if not title or not category or amount is None:
            return jsonify({
                "error": "Title, category, and amount are required"
            }), 400

        title = title.strip()
        category = category.strip()

        if not title or not category:
            return jsonify({
                "error": "Title and category cannot be empty"
            }), 400

        try:
            amount = float(amount)
        except (TypeError, ValueError):
            return jsonify({
                "error": "Amount must be a valid number"
            }), 400

        if amount <= 0:
            return jsonify({
                "error": "Amount must be greater than zero"
            }), 400

        if description is not None:
            description = description.strip()

        expense = Expense(
            user_id=current_user.id,
            title=title,
            category=category,
            amount=amount,
            description=description
        )

        db.session.add(expense)
        db.session.commit()

        return jsonify({
            "message": "Expense created successfully",
            "expense": {
                "id": expense.id,
                "user_id": expense.user_id,
                "title": expense.title,
                "category": expense.category,
                "amount": expense.amount,
                "description": expense.description,
                "expense_date": (
                    expense.expense_date.isoformat()
                    if expense.expense_date else None
                ),
                "created_at": (
                    expense.created_at.isoformat()
                    if expense.created_at else None
                )
            }
        }), 201

    # ----------------------------------------------
    # LIST EXPENSES
    # ----------------------------------------------

    user_expenses = Expense.query.filter_by(
        user_id=current_user.id
    ).all()

    return jsonify({
        "expenses": [
            {
                "id": expense.id,
                "user_id": expense.user_id,
                "title": expense.title,
                "category": expense.category,
                "amount": expense.amount,
                "description": expense.description,
                "expense_date": (
                    expense.expense_date.isoformat()
                    if expense.expense_date else None
                ),
                "created_at": (
                    expense.created_at.isoformat()
                    if expense.created_at else None
                )
            }
            for expense in user_expenses
        ]
    }), 200


# --------------------------------------------------
# GET SINGLE EXPENSE
# --------------------------------------------------

@expense_bp.route("/expenses/<int:expense_id>", methods=["GET"])
@login_required
def get_expense(expense_id):

    expense = Expense.query.filter_by(
        id=expense_id,
        user_id=current_user.id
    ).first()

    if expense is None:
        return jsonify({
            "error": "Expense not found"
        }), 404

    return jsonify({
        "expense": {
            "id": expense.id,
            "user_id": expense.user_id,
            "title": expense.title,
            "category": expense.category,
            "amount": expense.amount,
            "description": expense.description,
            "expense_date": (
                expense.expense_date.isoformat()
                if expense.expense_date else None
            ),
            "created_at": (
                expense.created_at.isoformat()
                if expense.created_at else None
            )
        }
    }), 200

# --------------------------------------------------
# UPDATE EXPENSE
# --------------------------------------------------

@expense_bp.route("/expenses/<int:expense_id>", methods=["PUT"])
@login_required
def update_expense(expense_id):

    expense = Expense.query.filter_by(
        id=expense_id,
        user_id=current_user.id
    ).first()

    if expense is None:
        return jsonify({
            "error": "Expense not found"
        }), 404

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must contain JSON"
        }), 400

    title = data.get("title")
    category = data.get("category")
    amount = data.get("amount")
    description = data.get("description")

    if title is not None:
        title = title.strip()

        if not title:
            return jsonify({
                "error": "Title cannot be empty"
            }), 400

        expense.title = title

    if category is not None:
        category = category.strip()

        if not category:
            return jsonify({
                "error": "Category cannot be empty"
            }), 400

        expense.category = category

    if amount is not None:
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            return jsonify({
                "error": "Amount must be a valid number"
            }), 400

        if amount <= 0:
            return jsonify({
                "error": "Amount must be greater than zero"
            }), 400

        expense.amount = amount

    if description is not None:
        expense.description = description.strip()

    db.session.commit()

    return jsonify({
        "message": "Expense updated successfully",
        "expense": {
            "id": expense.id,
            "user_id": expense.user_id,
            "title": expense.title,
            "category": expense.category,
            "amount": expense.amount,
            "description": expense.description,
            "expense_date": (
                expense.expense_date.isoformat()
                if expense.expense_date else None
            ),
            "created_at": (
                expense.created_at.isoformat()
                if expense.created_at else None
            )
        }
    }), 200

# --------------------------------------------------
# DELETE EXPENSE
# --------------------------------------------------

@expense_bp.route("/expenses/<int:expense_id>", methods=["DELETE"])
@login_required
def delete_expense(expense_id):

    expense = Expense.query.filter_by(
        id=expense_id,
        user_id=current_user.id
    ).first()

    if expense is None:
        return jsonify({
            "error": "Expense not found"
        }), 404

    db.session.delete(expense)
    db.session.commit()

    return jsonify({
        "message": "Expense deleted successfully"
    }), 200
