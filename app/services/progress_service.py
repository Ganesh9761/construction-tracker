from decimal import Decimal

from app.extensions import db
from app.models import Phase, ProgressUpdate, User


def create_progress_update(
    phase_id,
    completion_percentage,
    notes,
    updated_by,
):
    if completion_percentage is None:
        raise ValueError(
            "Completion percentage is required."
        )

    completion_percentage = Decimal(
        str(completion_percentage)
    )

    if completion_percentage < 0 or completion_percentage > 100:
        raise ValueError(
            "Completion percentage must be between 0 and 100."
        )

    notes = notes.strip() if notes else None

    phase = db.session.get(Phase, phase_id)

    if phase is None:
        raise ValueError("Phase not found.")

    user = db.session.get(User, updated_by)

    if user is None:
        raise ValueError("User not found.")

    if completion_percentage == 100:
        phase.status = "completed"
    elif completion_percentage > 0:
        phase.status = "in_progress"
    else:
        phase.status = "not_started"

    phase.completion_percentage = completion_percentage

    progress_update = ProgressUpdate(
        phase_id=phase_id,
        completion_percentage=completion_percentage,
        notes=notes,
        updated_by=updated_by,
    )

    db.session.add(progress_update)
    db.session.commit()

    return progress_update
