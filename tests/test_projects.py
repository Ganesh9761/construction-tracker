
from app.models import AuditLog


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
