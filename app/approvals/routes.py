from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from app.extensions import db
from app.models.approval import Approval


approval_bp = Blueprint("approvals", __name__)


# --------------------------------------------------
# LIST PENDING APPROVALS
# --------------------------------------------------

@approval_bp.route("/approvals", methods=["GET"])
@login_required
def approvals():

    if current_user.role != "admin":
        return jsonify({
            "error": "Forbidden",
            "message": "Admin access required"
        }), 403

    pending_approvals = Approval.query.filter_by(
        status="pending"
    ).all()

    return jsonify({
        "approvals": [
            {
                "id": approval.id,
                "expense_id": approval.expense_id,
                "approved_by": approval.approved_by,
                "status": approval.status,
                "remarks": approval.remarks,
                "created_at": (
                    approval.created_at.isoformat()
                    if approval.created_at else None
                )
            }
            for approval in pending_approvals
        ]
    }), 200


# --------------------------------------------------
# APPROVE EXPENSE
# --------------------------------------------------

@approval_bp.route(
    "/approvals/<int:approval_id>/approve",
    methods=["PUT"]
)
@login_required
def approve_expense(approval_id):

    if current_user.role != "admin":
        return jsonify({
            "error": "Forbidden",
            "message": "Admin access required"
        }), 403

    approval = Approval.query.get(approval_id)

    if approval is None:
        return jsonify({
            "error": "Approval not found"
        }), 404

    if approval.status != "pending":
        return jsonify({
            "error": "Approval already processed",
            "status": approval.status
        }), 400

    data = request.get_json(silent=True) or {}

    remarks = data.get("remarks")

    if remarks is not None:
        remarks = remarks.strip()

    approval.status = "approved"
    approval.approved_by = current_user.id
    approval.remarks = remarks

    db.session.commit()

    return jsonify({
        "message": "Expense approved successfully",
        "approval": {
            "id": approval.id,
            "expense_id": approval.expense_id,
            "approved_by": approval.approved_by,
            "status": approval.status,
            "remarks": approval.remarks,
            "created_at": (
                approval.created_at.isoformat()
                if approval.created_at else None
            )
        }
    }), 200


# --------------------------------------------------
# REJECT EXPENSE
# --------------------------------------------------

@approval_bp.route(
    "/approvals/<int:approval_id>/reject",
    methods=["PUT"]
)
@login_required
def reject_expense(approval_id):

    if current_user.role != "admin":
        return jsonify({
            "error": "Forbidden",
            "message": "Admin access required"
        }), 403

    approval = Approval.query.get(approval_id)

    if approval is None:
        return jsonify({
            "error": "Approval not found"
        }), 404

    if approval.status != "pending":
        return jsonify({
            "error": "Approval already processed",
            "status": approval.status
        }), 400

    data = request.get_json(silent=True) or {}

    remarks = data.get("remarks")

    if remarks is not None:
        remarks = remarks.strip()

    approval.status = "rejected"
    approval.approved_by = current_user.id
    approval.remarks = remarks

    db.session.commit()

    return jsonify({
        "message": "Expense rejected successfully",
        "approval": {
            "id": approval.id,
            "expense_id": approval.expense_id,
            "approved_by": approval.approved_by,
            "status": approval.status,
            "remarks": approval.remarks,
            "created_at": (
                approval.created_at.isoformat()
                if approval.created_at else None
            )
        }
    }), 200
