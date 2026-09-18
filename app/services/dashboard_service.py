from decimal import Decimal

from app.extensions import db
from app.models import Expense, Phase, Project


def get_dashboard_summary():
    total_projects = db.session.scalar(
        db.select(db.func.count(Project.id))
    ) or 0

    active_projects = db.session.scalar(
        db.select(db.func.count(Project.id))
        .where(Project.status == "active")
    ) or 0

    completed_projects = db.session.scalar(
        db.select(db.func.count(Project.id))
        .where(Project.status == "completed")
    ) or 0

    on_hold_projects = db.session.scalar(
        db.select(db.func.count(Project.id))
        .where(Project.status == "on_hold")
    ) or 0

    total_budget = db.session.scalar(
        db.select(
            db.func.coalesce(
                db.func.sum(Project.total_budget),
                0,
            )
        )
    )
    total_budget = Decimal(total_budget)

    total_actual_cost = db.session.scalar(
        db.select(
            db.func.coalesce(
                db.func.sum(Expense.amount),
                0,
            )
        )
    )
    total_actual_cost = Decimal(total_actual_cost)

    remaining_budget = total_budget - total_actual_cost

    if total_budget > 0:
        budget_utilization = (
            total_actual_cost / total_budget
        ) * Decimal("100")
    else:
        budget_utilization = Decimal("0")

    phases = db.session.scalars(
        db.select(Phase)
    ).all()

    total_allocated_budget = Decimal("0")
    weighted_progress = Decimal("0")

    for phase in phases:
        allocated_budget = Decimal(
            phase.allocated_budget
        )
        completion_percentage = Decimal(
            phase.completion_percentage
        )

        total_allocated_budget += allocated_budget
        weighted_progress += (
            allocated_budget * completion_percentage
        )

    if total_allocated_budget > 0:
        average_progress = (
            weighted_progress / total_allocated_budget
        )
    else:
        average_progress = Decimal("0")

    return {
        "total_projects": total_projects,
        "active_projects": active_projects,
        "completed_projects": completed_projects,
        "on_hold_projects": on_hold_projects,
        "total_budget": total_budget,
        "total_actual_cost": total_actual_cost,
        "remaining_budget": remaining_budget,
        "budget_utilization": budget_utilization,
        "average_progress": average_progress,
    }


def get_project_dashboard_rows():
    projects = db.session.scalars(
        db.select(Project)
        .order_by(Project.created_at.desc())
    ).all()

    project_rows = []

    for project in projects:
        total_budget = Decimal(project.total_budget)

        actual_cost = db.session.scalar(
            db.select(
                db.func.coalesce(
                    db.func.sum(Expense.amount),
                    0,
                )
            ).where(
                Expense.project_id == project.id
            )
        )
        actual_cost = Decimal(actual_cost)

        remaining_budget = total_budget - actual_cost

        if total_budget > 0:
            budget_utilization = (
                actual_cost / total_budget
            ) * Decimal("100")
        else:
            budget_utilization = Decimal("0")

        phases = db.session.scalars(
            db.select(Phase)
            .where(Phase.project_id == project.id)
        ).all()

        allocated_phase_budget = Decimal("0")
        weighted_progress = Decimal("0")

        for phase in phases:
            allocated_budget = Decimal(
                phase.allocated_budget
            )
            completion_percentage = Decimal(
                phase.completion_percentage
            )

            allocated_phase_budget += allocated_budget
            weighted_progress += (
                allocated_budget * completion_percentage
            )

        if allocated_phase_budget > 0:
            overall_progress = (
                weighted_progress / allocated_phase_budget
            )
        else:
            overall_progress = Decimal("0")

        project_rows.append(
            {
                "project_id": project.id,
                "project_name": project.name,
                "client_name": project.client_name,
                "status": project.status,
                "total_budget": total_budget,
                "actual_cost": actual_cost,
                "remaining_budget": remaining_budget,
                "budget_utilization": budget_utilization,
                "overall_progress": overall_progress,
            }
        )

    return project_rows


def get_project_chart_data():
    project_rows = get_project_dashboard_rows()

    return {
        "project_names": [
            row["project_name"]
            for row in project_rows
        ],
        "budgets": [
            float(row["total_budget"])
            for row in project_rows
        ],
        "actual_costs": [
            float(row["actual_cost"])
            for row in project_rows
        ],
        "progress": [
            float(row["overall_progress"])
            for row in project_rows
        ],
        "budget_utilization": [
            float(row["budget_utilization"])
            for row in project_rows
        ],
    }
