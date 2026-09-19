from flask import Blueprint, render_template
from flask_login import login_required

from app.services.authorization_service import permission_required
from app.services.dashboard_service import (
    get_dashboard_summary,
    get_project_chart_data,
    get_project_dashboard_rows,
)


main_bp = Blueprint("main", __name__)


@main_bp.route("/dashboard")
@login_required
@permission_required("view_dashboard")
def dashboard():
    dashboard_summary = get_dashboard_summary()
    project_dashboard_rows = get_project_dashboard_rows()
    project_chart_data = get_project_chart_data()

    return render_template(
        "main/dashboard.html",
        dashboard_summary=dashboard_summary,
        project_dashboard_rows=project_dashboard_rows,
        project_chart_data=project_chart_data,
    )
