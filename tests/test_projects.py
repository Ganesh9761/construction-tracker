import pytest

from app import create_app
from app.extensions import db
from app.models import AuditLog, User


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
def client(app):
    return app.test_client()


def login(client):
    response = client.post(
        "/auth/login",
        data={
            "email": "test@example.com",
            "password": "test-password",
        },
        follow_redirects=False,
    )

    assert response.status_code == 200


def test_project_creation_creates_audit_log(app, client):
    login(client)

    response = client.post(
        "/projects/new",
        data={
            "name": "Audit Test Construction Project",
            "client_name": "Test Client",
            "location": "Bengaluru, Karnataka",
            "start_date": "2026-09-18",
            "expected_completion_date": "2027-06-30",
            "total_budget": "10000000.00",
            "status": "planning",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    with app.app_context():
        logs = AuditLog.query.all()

        assert len(logs) == 1
        assert logs[0].action == "create"
        assert logs[0].entity_type == "project"
        assert logs[0].description == (
            "Created project "
            "'Audit Test Construction Project'."
        )
