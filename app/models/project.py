from datetime import datetime, timezone

from app.extensions import db


PROJECT_STATUSES = {
    "planning",
    "active",
    "on_hold",
    "completed",
    "cancelled",
}


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.String(150),
        nullable=False,
    )

    client_name = db.Column(
        db.String(120),
        nullable=False,
    )

    location = db.Column(
        db.String(200),
        nullable=False,
    )

    start_date = db.Column(
        db.Date,
        nullable=False,
    )

    expected_completion_date = db.Column(
        db.Date,
        nullable=False,
    )

    total_budget = db.Column(
        db.Numeric(14, 2),
        nullable=False,
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="planning",
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

    creator = db.relationship(
        "User",
        backref="projects",
    )

    def __repr__(self):
        return f"<Project {self.name}>"
