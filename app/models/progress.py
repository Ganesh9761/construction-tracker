from datetime import datetime, timezone

from app.extensions import db


class ProgressUpdate(db.Model):
    __tablename__ = "progress_updates"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    phase_id = db.Column(
        db.Integer,
        db.ForeignKey("phases.id"),
        nullable=False,
        index=True,
    )

    completion_percentage = db.Column(
        db.Numeric(5, 2),
        nullable=False,
    )

    notes = db.Column(
        db.Text,
        nullable=True,
    )

    updated_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    phase = db.relationship(
        "Phase",
        backref="progress_updates",
    )

    updater = db.relationship(
        "User",
        backref="progress_updates",
    )

    def __repr__(self):
        return (
            f"<ProgressUpdate "
            f"{self.phase_id} - "
            f"{self.completion_percentage}%>"
        )
