from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    first_name = db.Column(
        db.String(100),
        nullable=False
    )

    last_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(50),
        nullable=False,
        default="employee"
    )

    # Security questions
    security_question_1 = db.Column(
        db.String(255),
        nullable=True
    )

    security_answer_1_hash = db.Column(
        db.String(255),
        nullable=True
    )

    security_question_2 = db.Column(
        db.String(255),
        nullable=True
    )

    security_answer_2_hash = db.Column(
        db.String(255),
        nullable=True
    )

    security_question_3 = db.Column(
        db.String(255),
        nullable=True
    )

    security_answer_3_hash = db.Column(
        db.String(255),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    expenses = db.relationship(
        "Expense",
        backref="user",
        lazy=True,
        cascade="all, delete"
    )

    # -------------------------
    # Password methods
    # -------------------------

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )

    # -------------------------
    # Security answer methods
    # -------------------------

    def set_security_answer(self, question_number, answer):
        answer_hash = generate_password_hash(
            answer.strip().lower()
        )

        if question_number == 1:
            self.security_answer_1_hash = answer_hash

        elif question_number == 2:
            self.security_answer_2_hash = answer_hash

        elif question_number == 3:
            self.security_answer_3_hash = answer_hash

        else:
            raise ValueError(
                "Security question number must be 1, 2, or 3"
            )

    def check_security_answer(self, question_number, answer):
        answer = answer.strip().lower()

        if question_number == 1:
            answer_hash = self.security_answer_1_hash

        elif question_number == 2:
            answer_hash = self.security_answer_2_hash

        elif question_number == 3:
            answer_hash = self.security_answer_3_hash

        else:
            raise ValueError(
                "Security question number must be 1, 2, or 3"
            )

        if not answer_hash:
            return False

        return check_password_hash(
            answer_hash,
            answer
        )

    def __repr__(self):
        return f"<User {self.email}>"
