from datetime import datetime
from decimal import Decimal, InvalidOperation

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models import Project
from app.services.project_service import create_project


projects_bp = Blueprint("projects", __name__, url_prefix="/projects")


def can_manage_projects():
    return (
        current_user.is_authenticated
        and current_user.role in {"admin", "project_manager"}
    )


@projects_bp.route("/")
@login_required
def list_projects():
    projects = db.session.scalars(
        db.select(Project).order_by(Project.id.desc())
    ).all()

    return render_template(
        "projects/list.html",
        projects=projects,
    )


@projects_bp.route("/<int:project_id>")
@login_required
def detail(project_id):
    project = db.session.get(Project, project_id)

    if project is None:
        return "Project not found.", 404

    return render_template(
        "projects/detail.html",
        project=project,
    )


@projects_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if not can_manage_projects():
        return "Access denied.", 403

    if request.method == "POST":
        name = request.form.get("name", "")
        client_name = request.form.get("client_name", "")
        location = request.form.get("location", "")
        start_date_text = request.form.get("start_date", "")
        expected_completion_date_text = request.form.get(
            "expected_completion_date",
            "",
        )
        total_budget_text = request.form.get("total_budget", "")
        status = request.form.get("status", "planning")

        try:
            start_date = datetime.strptime(
                start_date_text,
                "%Y-%m-%d",
            ).date()

            expected_completion_date = datetime.strptime(
                expected_completion_date_text,
                "%Y-%m-%d",
            ).date()

            total_budget = Decimal(total_budget_text)

            project = create_project(
                name=name,
                client_name=client_name,
                location=location,
                start_date=start_date,
                expected_completion_date=expected_completion_date,
                total_budget=total_budget,
                created_by=current_user.id,
                status=status,
            )

        except (ValueError, InvalidOperation) as error:
            flash(str(error), "error")

            return render_template(
                "projects/create.html"
            ), 400

        flash(
            f"Project '{project.name}' created successfully.",
            "success",
        )

        return redirect(
            url_for("projects.list_projects")
        )

    return render_template("projects/create.html")
