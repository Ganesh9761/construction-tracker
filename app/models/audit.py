from datetime import datetime, timezone

from app.extensions import db


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    action = db.Column(
        db.String(50),
        nullable=False,
        index=True,
    )

    entity_type = db.Column(
        db.String(50),
        nullable=False,
        index=True,
    )

    entity_id = db.Column(
        db.Integer,
        nullable=True,
        index=True,
    )

    description = db.Column(
        db.Text,
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

    user = db.relationship(
        "User",
        backref="audit_logs",
    )

    def __repr__(self):
        return (
            f"<AuditLog "
            f"{self.action} "
            f"{self.entity_type}:{self.entity_id}>"
        )
