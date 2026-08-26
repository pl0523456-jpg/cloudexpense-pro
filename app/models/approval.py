from datetime import datetime
from app.extensions import db


class Approval(db.Model):
    __tablename__ = "approvals"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    expense_id = db.Column(
        db.Integer,
        db.ForeignKey("expenses.id"),
        nullable=False
    )

    approved_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="pending"
    )

    remarks = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


    def __repr__(self):
        return f"<Approval {self.status}>"
