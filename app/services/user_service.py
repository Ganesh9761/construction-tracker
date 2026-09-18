from app.extensions import db
from app.models import User


ALLOWED_ROLES = {
    "admin",
    "project_manager",
    "site_engineer",
}


def create_user(username, email, password, role="site_engineer"):
    username = username.strip()
    email = email.strip().lower()

    if not username:
        raise ValueError("Username is required.")

    if not email:
        raise ValueError("Email is required.")

    if not password:
        raise ValueError("Password is required.")

    if role not in ALLOWED_ROLES:
        raise ValueError("Invalid user role.")

    existing_username = db.session.scalar(
        db.select(User).where(User.username == username)
    )

    if existing_username:
        raise ValueError("Username already exists.")

    existing_email = db.session.scalar(
        db.select(User).where(User.email == email)
    )

    if existing_email:
        raise ValueError("Email already exists.")

    user = User(
        username=username,
        email=email,
        role=role,
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return user
