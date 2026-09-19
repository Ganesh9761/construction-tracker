from datetime import datetime
from decimal import Decimal, InvalidOperation

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.extensions import db
from app.models import Phase, Project
from app.services.authorization_service import permission_required
from app.services.phase_service import create_phase


phases_bp = Blueprint(
    "phases",
    __name__,
    url_prefix="/projects/<int:project_id>/phases",
)


@phases_bp.route("/")
@login_required
@permission_required("view_projects")
def list_phases(project_id):
    project = db.session.get(Project, project_id)

    if project is None:
        return "Project not found.", 404

    phases = db.session.scalars(
        db.select(Phase)
        .where(Phase.project_id == project_id)
        .order_by(Phase.id)
    ).all()

    return render_template(
        "phases/list.html",
        project=project,
        phases=phases,
    )


@phases_bp.route("/create", methods=["GET", "POST"])
@login_required
@permission_required("manage_phases")
def create(project_id):
    project = db.session.get(Project, project_id)

    if project is None:
        return "Project not found.", 404

    if request.method == "POST":
        name = request.form.get("name", "")
        description = request.form.get("description", "")

        start_date_text = request.form.get(
            "start_date",
            "",
        )

        expected_completion_date_text = request.form.get(
            "expected_completion_date",
            "",
        )

        allocated_budget_text = request.form.get(
            "allocated_budget",
            "",
        )

        completion_percentage_text = request.form.get(
            "completion_percentage",
            "0",
        )

        status = request.form.get(
            "status",
            "not_started",
        )

        try:
            start_date = datetime.strptime(
                start_date_text,
                "%Y-%m-%d",
            ).date()

            expected_completion_date = datetime.strptime(
                expected_completion_date_text,
                "%Y-%m-%d",
            ).date()

            allocated_budget = Decimal(
                allocated_budget_text
            )

            completion_percentage = Decimal(
                completion_percentage_text
            )

            phase = create_phase(
                project_id=project_id,
                name=name,
                description=description,
                allocated_budget=allocated_budget,
                start_date=start_date,
                expected_completion_date=expected_completion_date,
                completion_percentage=completion_percentage,
                status=status,
            )

        except (ValueError, InvalidOperation) as error:
            flash(str(error), "error")

            return render_template(
                "phases/create.html",
                project=project,
            ), 400

        flash(
            f"Phase '{phase.name}' created successfully.",
            "success",
        )

        return redirect(
            url_for(
                "phases.list_phases",
                project_id=project_id,
            )
        )

    return render_template(
        "phases/create.html",
        project=project,
    )
