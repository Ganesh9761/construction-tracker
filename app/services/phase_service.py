from app.extensions import db
from app.models import Phase, Project
from app.models.phase import PHASE_STATUSES


def create_phase(
    project_id,
    name,
    description,
    allocated_budget,
    start_date,
    expected_completion_date,
    completion_percentage=0,
    status="not_started",
):
    name = name.strip()
    description = description.strip() if description else None

    if not name:
        raise ValueError("Phase name is required.")

    if allocated_budget is None or allocated_budget <= 0:
        raise ValueError("Phase budget must be greater than zero.")

    if start_date is None:
        raise ValueError("Phase start date is required.")

    if expected_completion_date is None:
        raise ValueError("Phase completion date is required.")

    if expected_completion_date < start_date:
        raise ValueError(
            "Phase completion date cannot be before start date."
        )

    if completion_percentage is None:
        completion_percentage = 0

    if completion_percentage < 0 or completion_percentage > 100:
        raise ValueError(
            "Completion percentage must be between 0 and 100."
        )

    if status not in PHASE_STATUSES:
        raise ValueError("Invalid phase status.")

    project = db.session.get(Project, project_id)

    if project is None:
        raise ValueError("Project not found.")

    existing_budget = db.session.scalar(
        db.select(
            db.func.coalesce(
                db.func.sum(Phase.allocated_budget),
                0,
            )
        ).where(
            Phase.project_id == project_id
        )
    )

    total_allocated_budget = existing_budget + allocated_budget

    if total_allocated_budget > project.total_budget:
        raise ValueError(
            "Total phase budgets cannot exceed the project budget."
        )

    phase = Phase(
        project_id=project_id,
        name=name,
        description=description,
        allocated_budget=allocated_budget,
        start_date=start_date,
        expected_completion_date=expected_completion_date,
        completion_percentage=completion_percentage,
        status=status,
    )

    db.session.add(phase)
    db.session.commit()

    return phase
