from flask import Blueprint, render_template
from flask_login import login_required

from app.extensions import db
from app.models import Phase, Project
from app.services.authorization_service import permission_required
from app.services.phase_finance_service import (
    get_phase_financial_summary,
)


phase_finance_bp = Blueprint(
    "phase_finance",
    __name__,
    url_prefix="/projects/<int:project_id>/phases/<int:phase_id>/finance",
)


@phase_finance_bp.route("/")
@login_required
@permission_required("view_financial_analysis")
def detail(project_id, phase_id):
    project = db.session.get(Project, project_id)

    if project is None:
        return "Project not found.", 404

    phase = db.session.get(Phase, phase_id)

    if phase is None:
        return "Phase not found.", 404

    if phase.project_id != project_id:
        return "Phase does not belong to this project.", 403

    financial_summary = get_phase_financial_summary(
        phase_id
    )

    return render_template(
        "phase_finance/detail.html",
        project=project,
        phase=phase,
        financial_summary=financial_summary,
    )
