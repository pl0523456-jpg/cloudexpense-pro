from flask import Blueprint, request, jsonify, send_file
from uuid import uuid4
from flask_login import login_required, current_user

from app.extensions import db
from app.models.expense import Expense
from app.models.approval import Approval
from app.services.s3_service import upload_receipt, download_receipt


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

        # ------------------------------------------
        # CREATE EXPENSE
        # ------------------------------------------

        expense = Expense(
            user_id=current_user.id,
            title=title,
            category=category,
            amount=amount,
            description=description
        )

        db.session.add(expense)

        # Make sure expense.id is generated
        # before creating the approval record.
        db.session.flush()

        # ------------------------------------------
        # CREATE PENDING APPROVAL
        # ------------------------------------------

        approval = Approval(
            expense_id=expense.id,
            status="pending"
        )

        db.session.add(approval)

        # Save Expense and Approval together
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

# --------------------------------------------------
# UPLOAD EXPENSE RECEIPT
# --------------------------------------------------

@expense_bp.route("/expenses/<int:expense_id>/receipt", methods=["POST"])
@login_required
def upload_expense_receipt(expense_id):

    expense = Expense.query.filter_by(
        id=expense_id,
        user_id=current_user.id
    ).first()

    if expense is None:
        return jsonify({
            "error": "Expense not found"
        }), 404

    file = request.files.get("receipt")

    if file is None:
        return jsonify({
            "error": "Receipt file is required"
        }), 400

    if not file.filename:
        return jsonify({
            "error": "Receipt filename is required"
        }), 400

    file_extension = ""

    if "." in file.filename:
        file_extension = "." + file.filename.rsplit(".", 1)[1].lower()

    object_key = (
        f"receipts/user-{current_user.id}/"
        f"expense-{expense.id}/"
        f"{uuid4().hex}{file_extension}"
    )

    upload_receipt(
        file.stream,
        object_key,
        file.content_type
    )

    expense.receipt_url = object_key
    db.session.commit()

    return jsonify({
        "message": "Receipt uploaded successfully",
        "expense_id": expense.id,
        "receipt_url": expense.receipt_url
    }), 200

# --------------------------------------------------
# DOWNLOAD EXPENSE RECEIPT
# --------------------------------------------------

@expense_bp.route(
    "/expenses/<int:expense_id>/receipt",
    methods=["GET"]
)
@login_required
def download_expense_receipt(expense_id):

    expense = Expense.query.filter_by(
        id=expense_id,
        user_id=current_user.id
    ).first()

    if expense is None:
        return jsonify({
            "error": "Expense not found"
        }), 404

    if not expense.receipt_url:
        return jsonify({
            "error": "No receipt attached to this expense"
        }), 404

    try:
        response = download_receipt(expense.receipt_url)

        return send_file(
            response["Body"],
            mimetype=response.get(
                "ContentType",
                "application/octet-stream"
            ),
            as_attachment=True,
            download_name=f"expense-{expense.id}-receipt"
        )

    except Exception:
        return jsonify({
            "error": "Unable to download receipt"
        }), 500
