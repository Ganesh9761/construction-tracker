from flask_login import login_user

from app.extensions import db
from app.models import User
from app.services.authorization_service import has_permission


def create_user(role):
    user = User(
        username=f"{role}_user",
        email=f"{role}@example.com",
        role=role,
    )
    user.set_password("test-password")
    db.session.add(user)
    db.session.commit()
    return user


def test_admin_has_manage_users_permission(app):
    with app.test_request_context():
        user = create_user("admin")
        login_user(user)

        assert has_permission("manage_users") is True


def test_project_manager_cannot_manage_users(app):
    with app.test_request_context():
        user = create_user("project_manager")
        login_user(user)

        assert has_permission("manage_users") is False


def test_site_engineer_can_create_expense(app):
    with app.test_request_context():
        user = create_user("site_engineer")
        login_user(user)

        assert has_permission("create_expense") is True


def test_site_engineer_cannot_edit_project(app):
    with app.test_request_context():
        user = create_user("site_engineer")
        login_user(user)

        assert has_permission("edit_project") is False


def test_site_engineer_cannot_access_user_management(app, client):
    with app.app_context():
        user = create_user("site_engineer")
        user_id = user.id

    with client.session_transaction() as session:
        session["_user_id"] = str(user_id)
        session["_fresh"] = True

    response = client.get("/users/")

    assert response.status_code == 403


def test_admin_can_access_user_management(app, client):
    with app.app_context():
        user = create_user("admin")
        user_id = user.id

    with client.session_transaction() as session:
        session["_user_id"] = str(user_id)
        session["_fresh"] = True

    response = client.get("/users/")

    assert response.status_code == 200
