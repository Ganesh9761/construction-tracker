from datetime import datetime
from decimal import Decimal, InvalidOperation

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models import Project
from app.models.project import PROJECT_STATUSES
from app.services.expense_service import (
    get_expense_category_summary,
    get_monthly_expense_summary,
)
from app.services.project_finance_service import (
    get_project_financial_summary,
    get_project_phase_financials,
    get_project_progress_summary,
)
from app.services.project_service import create_project


projects_bp = Blueprint(
    "projects",
    __name__,
    url_prefix="/projects",
)


@projects_bp.route("/")
@login_required
def list_projects():
    projects = db.session.scalars(
        db.select(Project)
        .order_by(Project.created_at.desc())
    ).all()

    return render_template(
        "projects/list.html",
        projects=projects,
    )


@projects_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if current_user.role not in {"admin", "project_manager"}:
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
                "projects/create.html",
                statuses=sorted(PROJECT_STATUSES),
            ), 400

        flash(
            f"Project #{project.id} created successfully.",
            "success",
        )

        return redirect(
            url_for(
                "projects.detail",
                project_id=project.id,
            )
        )

    return render_template(
        "projects/create.html",
        statuses=sorted(PROJECT_STATUSES),
    )


@projects_bp.route("/<int:project_id>")
@login_required
def detail(project_id):
    project = db.session.get(Project, project_id)

    if project is None:
        return "Project not found.", 404

    financial_summary = get_project_financial_summary(
        project_id
    )

    phase_financials = get_project_phase_financials(
        project_id
    )

    expense_category_summary = get_expense_category_summary(
        project_id
    )

    monthly_expense_summary = get_monthly_expense_summary(
        project_id
    )

    progress_summary = get_project_progress_summary(
        project_id
    )

    return render_template(
        "projects/detail.html",
        project=project,
        financial_summary=financial_summary,
        phase_financials=phase_financials,
        expense_category_summary=expense_category_summary,
        monthly_expense_summary=monthly_expense_summary,
        progress_summary=progress_summary,
    )
