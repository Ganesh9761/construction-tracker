from app.extensions import db
from app.models import AuditLog, User


def create_audit_log(
    user_id,
    action,
    entity_type,
    entity_id,
    description,
):
    if not action or not action.strip():
        raise ValueError("Audit action is required.")

    if not entity_type or not entity_type.strip():
        raise ValueError("Audit entity type is required.")

    if not description or not description.strip():
        raise ValueError("Audit description is required.")

    user = db.session.get(User, user_id)

    if user is None:
        raise ValueError("User not found.")

    audit_log = AuditLog(
        user_id=user_id,
        action=action.strip().lower(),
        entity_type=entity_type.strip().lower(),
        entity_id=entity_id,
        description=description.strip(),
    )

    db.session.add(audit_log)

    return audit_log


def get_entity_audit_logs(
    entity_type,
    entity_id,
):
    return db.session.scalars(
        db.select(AuditLog)
        .where(
            AuditLog.entity_type == entity_type.strip().lower(),
            AuditLog.entity_id == entity_id,
        )
        .order_by(
            AuditLog.created_at.desc()
        )
    ).all()


def get_recent_audit_logs(limit=50):
    if limit <= 0:
        raise ValueError("Audit log limit must be greater than zero.")

    return db.session.scalars(
        db.select(AuditLog)
        .order_by(
            AuditLog.created_at.desc()
        )
        .limit(limit)
    ).all()
