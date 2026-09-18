import pytest

from app import create_app
from app.extensions import db
from app.models import AuditLog, User
from app.services.audit_service import (
    create_audit_log,
    get_entity_audit_logs,
    get_recent_audit_logs,
)


class TestConfig:
    TESTING = True
    SECRET_KEY = "test-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False


@pytest.fixture
def app():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()

        user = User(
            username="test_admin",
            email="test@example.com",
            role="admin",
            is_active=True,
        )
        user.set_password("test-password")

        db.session.add(user)
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def user(app):
    return db.session.scalar(
        db.select(User)
        .where(User.username == "test_admin")
    )


def test_create_audit_log(app, user):
    audit_log = create_audit_log(
        user_id=user.id,
        action="create",
        entity_type="project",
        entity_id=1,
        description="Created test project.",
    )

    assert audit_log.id is not None
    assert audit_log.user_id == user.id
    assert audit_log.action == "create"
    assert audit_log.entity_type == "project"
    assert audit_log.entity_id == 1
    assert audit_log.description == "Created test project."


def test_get_entity_audit_logs(app, user):
    create_audit_log(
        user_id=user.id,
        action="create",
        entity_type="project",
        entity_id=1,
        description="Created test project.",
    )

    logs = get_entity_audit_logs(
        entity_type="project",
        entity_id=1,
    )

    assert len(logs) == 1
    assert logs[0].entity_type == "project"
    assert logs[0].entity_id == 1


def test_get_recent_audit_logs(app, user):
    create_audit_log(
        user_id=user.id,
        action="create",
        entity_type="project",
        entity_id=1,
        description="Created test project.",
    )

    create_audit_log(
        user_id=user.id,
        action="update",
        entity_type="project",
        entity_id=1,
        description="Updated test project.",
    )

    logs = get_recent_audit_logs()

    assert len(logs) == 2
    assert logs[0].action == "update"
    assert logs[1].action == "create"


def test_create_audit_log_requires_valid_user(app):
    with pytest.raises(ValueError, match="User not found."):
        create_audit_log(
            user_id=9999,
            action="create",
            entity_type="project",
            entity_id=1,
            description="Invalid user test.",
        )


def test_create_audit_log_requires_action(app, user):
    with pytest.raises(
        ValueError,
        match="Audit action is required.",
    ):
        create_audit_log(
            user_id=user.id,
            action="",
            entity_type="project",
            entity_id=1,
            description="Invalid action test.",
        )
