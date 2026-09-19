from flask import Blueprint, render_template
from flask_login import login_required

from app.services.audit_service import get_recent_audit_logs
from app.services.authorization_service import permission_required


audit_bp = Blueprint(
    "audit",
    __name__,
    url_prefix="/audit-logs",
)


@audit_bp.route("/")
@login_required
@permission_required("view_audit_logs")
def list_logs():
    audit_logs = get_recent_audit_logs()

    return render_template(
        "audit/list.html",
        audit_logs=audit_logs,
    )
