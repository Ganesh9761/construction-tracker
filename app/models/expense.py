from datetime import datetime, timezone

from app.extensions import db


EXPENSE_CATEGORIES = {
    "materials",
    "labor",
    "equipment",
    "transport",
    "subcontractor",
    "permits",
    "utilities",
    "other",
}

PAYMENT_STATUSES = {
    "pending",
    "paid",
    "partially_paid",
    "cancelled",
}


class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    project_id = db.Column(
        db.Integer,
        db.ForeignKey("projects.id"),
        nullable=False,
        index=True,
    )

    phase_id = db.Column(
        db.Integer,
        db.ForeignKey("phases.id"),
        nullable=False,
        index=True,
    )

    expense_date = db.Column(
        db.Date,
        nullable=False,
    )

    category = db.Column(
        db.String(40),
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=False,
    )

    amount = db.Column(
        db.Numeric(14, 2),
        nullable=False,
    )

    vendor_name = db.Column(
        db.String(150),
        nullable=False,
    )

    payment_status = db.Column(
        db.String(30),
        nullable=False,
        default="pending",
    )

    created_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    project = db.relationship(
        "Project",
        backref="expenses",
    )

    phase = db.relationship(
        "Phase",
        backref="expenses",
    )

    creator = db.relationship(
        "User",
        backref="expenses",
    )

    def __repr__(self):
        return f"<Expense {self.id} - {self.amount}>"
