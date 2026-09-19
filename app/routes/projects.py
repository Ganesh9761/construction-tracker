from datetime import datetime, timezone

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, ValidationError

from app.extensions import db
from app.models import Expense, Project
from app.services.audit_service import create_audit_log
from app.services.authorization_service import permission_required
from app.services.project_finance_service import (
    get_project_cost_escalation,
    get_project_financial_summary,
    get_project_phase_financials,
    get_project_progress_summary,
)


projects_bp = Blueprint(
    "projects",
    __name__,
    url_prefix="/projects",
)


class ProjectForm(FlaskForm):
    name = StringField(
        "Project Name",
        validators=[DataRequired()],
    )

    client_name = StringField(
        "Client Name",
        validators=[DataRequired()],
    )

    location = StringField(
        "Location",
        validators=[DataRequired()],
    )

    start_date = DateField(
        "Start Date",
        format="%Y-%m-%d",
        validators=[DataRequired()],
    )

    expected_completion_date = DateField(
        "Expected Completion Date",
        format="%Y-%m-%d",
        validators=[DataRequired()],
    )

    total_budget = DecimalField(
        "Total Budget",
        places=2,
        validators=[
            DataRequired(),
            NumberRange(
                min=0,
                message="Budget must be zero or greater.",
            ),
        ],
    )

    status = SelectField(
        "Status",
        choices=[
            ("planning", "Planning"),
            ("active", "Active"),
            ("on_hold", "On Hold"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        validators=[DataRequired()],
    )

    submit = SubmitField("Save Project")

    def validate_expected_completion_date(self, field):
        if (
            self.start_date.data
            and field.data
            and field.data < self.start_date.data
        ):
            raise ValidationError(
                "Expected completion date cannot be before the start date."
            )


@projects_bp.route("/")
@login_required
@permission_required("view_projects")
def list_projects():
    projects = db.session.scalars(
        db.select(Project).order_by(Project.id)
    ).all()

    return render_template(
        "projects/list.html",
        projects=projects,
    )


@projects_bp.route("/new", methods=["GET", "POST"])
@login_required
@permission_required("create_project")
def create():
    form = ProjectForm()

    if form.validate_on_submit():
        now = datetime.now(timezone.utc)

        project = Project(
            name=form.name.data.strip(),
            client_name=form.client_name.data.strip(),
            location=form.location.data.strip(),
            start_date=form.start_date.data,
            expected_completion_date=form.expected_completion_date.data,
            total_budget=form.total_budget.data,
            status=form.status.data,
            created_by=current_user.id,
            created_at=now,
            updated_at=now,
        )

        db.session.add(project)
        db.session.flush()

        create_audit_log(
            user_id=current_user.id,
            action="create",
            entity_type="project",
            entity_id=project.id,
            description=f"Created project '{project.name}'.",
        )

        db.session.commit()

        flash(
            "Project created successfully.",
            "success",
        )

        return redirect(
            url_for("projects.list_projects")
        )

    if form.is_submitted():
        flash(
            "Please correct the highlighted project details.",
            "error",
        )

        return render_template(
            "projects/form.html",
            form=form,
            project=None,
        ), 400

    return render_template(
        "projects/form.html",
        form=form,
        project=None,
    )


@projects_bp.route("/<int:project_id>")
@login_required
@permission_required("view_projects")
def detail(project_id):
    project = db.session.get(
        Project,
        project_id,
    )

    if project is None:
        return "Project not found.", 404

    financial_summary = get_project_financial_summary(
        project_id
    )

    phase_financials = get_project_phase_financials(
        project_id
    )

    progress_summary = get_project_progress_summary(
        project_id
    )

    expenses = db.session.scalars(
        db.select(Expense)
        .where(
            Expense.project_id == project_id
        )
        .order_by(
            Expense.expense_date.asc(),
            Expense.id.asc(),
        )
    ).all()

    expense_category_summary = {}

    for expense in expenses:
        category = expense.category

        expense_category_summary[category] = (
            expense_category_summary.get(category, 0)
            + expense.amount
        )

    monthly_expense_summary = {}

    for expense in expenses:
        month = expense.expense_date.strftime(
            "%Y-%m"
        )

        monthly_expense_summary[month] = (
            monthly_expense_summary.get(month, 0)
            + expense.amount
        )

    monthly_expense_summary = [
        {
            "month": month,
            "total": total,
        }
        for month, total in sorted(
            monthly_expense_summary.items()
        )
    ]

    cost_escalation = get_project_cost_escalation(
        project_id
    )

    return render_template(
        "projects/detail.html",
        project=project,
        financial_summary=financial_summary,
        phase_financials=phase_financials,
        progress_summary=progress_summary,
        expense_category_summary=expense_category_summary,
        monthly_expense_summary=monthly_expense_summary,
        cost_escalation=cost_escalation,
        expense_count=len(expenses),
    )


@projects_bp.route(
    "/<int:project_id>/edit",
    methods=["GET", "POST"],
)
@login_required
@permission_required("edit_project")
def edit(project_id):
    project = db.session.get(
        Project,
        project_id,
    )

    if project is None:
        return "Project not found.", 404

    form = ProjectForm(obj=project)

    if form.validate_on_submit():
        old_name = project.name

        project.name = form.name.data.strip()
        project.client_name = form.client_name.data.strip()
        project.location = form.location.data.strip()
        project.start_date = form.start_date.data
        project.expected_completion_date = (
            form.expected_completion_date.data
        )
        project.total_budget = form.total_budget.data
        project.status = form.status.data
        project.updated_at = datetime.now(timezone.utc)

        create_audit_log(
            user_id=current_user.id,
            action="update",
            entity_type="project",
            entity_id=project.id,
            description=f"Updated project '{old_name}'.",
        )

        db.session.commit()

        flash(
            "Project updated successfully.",
            "success",
        )

        return redirect(
            url_for(
                "projects.detail",
                project_id=project.id,
            )
        )

    if form.is_submitted():
        flash(
            "Please correct the highlighted project details.",
            "error",
        )

        return render_template(
            "projects/form.html",
            form=form,
            project=project,
        )

    return render_template(
        "projects/form.html",
        form=form,
        project=project,
    )
