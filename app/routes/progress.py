from decimal import Decimal, InvalidOperation

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models import Phase, ProgressUpdate, Project
from app.services.progress_service import create_progress_update


progress_bp = Blueprint(
    "progress",
    __name__,
    url_prefix="/projects/<int:project_id>/phases/<int:phase_id>/progress",
)


@progress_bp.route("/")
@login_required
def list_progress(project_id, phase_id):
    project = db.session.get(Project, project_id)

    if project is None:
        return "Project not found.", 404

    phase = db.session.get(Phase, phase_id)

    if phase is None:
        return "Phase not found.", 404

    if phase.project_id != project_id:
        return "Phase does not belong to this project.", 403

    progress_updates = db.session.scalars(
        db.select(ProgressUpdate)
        .where(ProgressUpdate.phase_id == phase_id)
        .order_by(
            ProgressUpdate.created_at.desc(),
            ProgressUpdate.id.desc(),
        )
    ).all()

    return render_template(
        "progress/list.html",
        project=project,
        phase=phase,
        progress_updates=progress_updates,
    )


@progress_bp.route("/create", methods=["GET", "POST"])
@login_required
def create(project_id, phase_id):
    project = db.session.get(Project, project_id)

    if project is None:
        return "Project not found.", 404

    phase = db.session.get(Phase, phase_id)

    if phase is None:
        return "Phase not found.", 404

    if phase.project_id != project_id:
        return "Phase does not belong to this project.", 403

    if request.method == "POST":
        completion_percentage_text = request.form.get(
            "completion_percentage",
            "",
        )

        notes = request.form.get(
            "notes",
            "",
        )

        try:
            completion_percentage = Decimal(
                completion_percentage_text
            )

            progress_update = create_progress_update(
                phase_id=phase_id,
                completion_percentage=completion_percentage,
                notes=notes,
                updated_by=current_user.id,
            )

        except (ValueError, InvalidOperation) as error:
            flash(str(error), "error")

            return render_template(
                "progress/create.html",
                project=project,
                phase=phase,
            ), 400

        flash(
            (
                f"Progress update #{progress_update.id} "
                "created successfully."
            ),
            "success",
        )

        return redirect(
            url_for(
                "progress.list_progress",
                project_id=project_id,
                phase_id=phase_id,
            )
        )

    return render_template(
        "progress/create.html",
        project=project,
        phase=phase,
    )
