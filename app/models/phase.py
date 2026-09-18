from datetime import datetime, timezone

from app.extensions import db


PHASE_STATUSES = {
    "not_started",
    "in_progress",
    "on_hold",
    "completed",
}


class Phase(db.Model):
    __tablename__ = "phases"

    id = db.Column(db.Integer, primary_key=True)

    project_id = db.Column(
        db.Integer,
        db.ForeignKey("projects.id"),
        nullable=False,
        index=True,
    )

    name = db.Column(
        db.String(120),
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=True,
    )

    allocated_budget = db.Column(
        db.Numeric(14, 2),
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

    completion_percentage = db.Column(
        db.Numeric(5, 2),
        nullable=False,
        default=0,
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="not_started",
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
        backref="phases",
    )

    def __repr__(self):
        return f"<Phase {self.name}>"
