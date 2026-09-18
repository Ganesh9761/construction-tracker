from app.extensions import db
from app.models import Project
from app.models.project import PROJECT_STATUSES


def create_project(
    name,
    client_name,
    location,
    start_date,
    expected_completion_date,
    total_budget,
    created_by,
    status="planning",
):
    name = name.strip()
    client_name = client_name.strip()
    location = location.strip()

    if not name:
        raise ValueError("Project name is required.")

    if not client_name:
        raise ValueError("Client name is required.")

    if not location:
        raise ValueError("Project location is required.")

    if start_date is None:
        raise ValueError("Start date is required.")

    if expected_completion_date is None:
        raise ValueError("Expected completion date is required.")

    if expected_completion_date < start_date:
        raise ValueError(
            "Expected completion date cannot be before start date."
        )

    if total_budget is None or total_budget <= 0:
        raise ValueError("Project budget must be greater than zero.")

    if status not in PROJECT_STATUSES:
        raise ValueError("Invalid project status.")

    project = Project(
        name=name,
        client_name=client_name,
        location=location,
        start_date=start_date,
        expected_completion_date=expected_completion_date,
        total_budget=total_budget,
        status=status,
        created_by=created_by,
    )

    db.session.add(project)
    db.session.commit()

    return project
