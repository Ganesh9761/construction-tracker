from flask import Blueprint, render_template
from flask_login import login_required

from app.extensions import db
from app.models import Project
from app.services.project_finance_service import (
    get_project_cost_escalation,
    get_project_phase_financials,
    get_project_progress_summary,
)


phase_analysis_bp = Blueprint(
    "phase_analysis",
    __name__,
    url_prefix="/projects",
)


@phase_analysis_bp.route(
    "/<int:project_id>/analysis"
)
@login_required
def detail(project_id):
    project = db.session.get(
        Project,
        project_id,
    )

    if project is None:
        return "Project not found.", 404

    phase_financials = get_project_phase_financials(
        project_id
    )

    progress_summary = get_project_progress_summary(
        project_id
    )

    cost_escalation = get_project_cost_escalation(
        project_id
    )

    return render_template(
        "phase_analysis/detail.html",
        project=project,
        phase_financials=phase_financials,
        progress_summary=progress_summary,
        cost_escalation=cost_escalation,
    )
