from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.extensions import db
from app.models import User
from app.services.authorization_service import permission_required
from app.services.user_service import create_user


users_bp = Blueprint(
    "users",
    __name__,
    url_prefix="/users",
)


@users_bp.route("/create", methods=["GET", "POST"])
@login_required
@permission_required("manage_users")
def create():
    if request.method == "POST":
        username = request.form.get("username", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        role = request.form.get("role", "site_engineer")

        try:
            user = create_user(
                username=username,
                email=email,
                password=password,
                role=role,
            )
        except ValueError as error:
            flash(str(error), "error")
            return render_template(
                "users/create.html"
            ), 400

        flash(
            f"User '{user.username}' created successfully.",
            "success",
        )

        return redirect(
            url_for("users.create")
        )

    return render_template("users/create.html")


@users_bp.route("/")
@login_required
@permission_required("manage_users")
def list_users():
    users = db.session.scalars(
        db.select(User).order_by(User.id)
    ).all()

    return render_template(
        "users/list.html",
        users=users,
    )
