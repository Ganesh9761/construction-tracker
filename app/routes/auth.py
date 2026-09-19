from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)

from app.extensions import db
from app.models import User


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(
            url_for("main.dashboard")
        )

    if request.method == "POST":
        email = request.form.get(
            "email",
            "",
        ).strip().lower()

        password = request.form.get(
            "password",
            "",
        )

        user = db.session.scalar(
            db.select(User).where(
                User.email == email
            )
        )

        if user is None or not user.check_password(password):
            flash(
                "Invalid email or password.",
                "error",
            )

            return render_template(
                "auth/login.html"
            ), 401

        if not user.is_active:
            flash(
                "This account is inactive.",
                "error",
            )

            return render_template(
                "auth/login.html"
            ), 403

        login_user(user)

        return redirect(
            url_for("main.dashboard")
        )

    return render_template(
        "auth/login.html"
    )


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()

    flash(
        "You have been signed out successfully.",
        "success",
    )

    return redirect(
        url_for("auth.login")
    )
