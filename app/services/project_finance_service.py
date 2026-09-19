from collections import defaultdict
from decimal import Decimal

from app.extensions import db
from app.models import Expense, Phase, Project


def get_project_financial_summary(project_id):
    project = db.session.get(Project, project_id)

    if project is None:
        raise ValueError("Project not found.")

    actual_cost = db.session.scalar(
        db.select(
            db.func.coalesce(
                db.func.sum(Expense.amount),
                0,
            )
        ).where(
            Expense.project_id == project_id
        )
    )

    actual_cost = Decimal(actual_cost)

    total_budget = Decimal(project.total_budget)

    remaining_budget = total_budget - actual_cost

    if total_budget > 0:
        budget_utilization = (
            actual_cost / total_budget
        ) * Decimal("100")
    else:
        budget_utilization = Decimal("0")

    budget_variance = total_budget - actual_cost

    return {
        "total_budget": total_budget,
        "actual_cost": actual_cost,
        "remaining_budget": remaining_budget,
        "budget_variance": budget_variance,
        "budget_utilization": budget_utilization,
    }


def get_project_phase_financials(project_id):
    project = db.session.get(Project, project_id)

    if project is None:
        raise ValueError("Project not found.")

    phases = db.session.scalars(
        db.select(Phase)
        .where(Phase.project_id == project_id)
        .order_by(Phase.id)
    ).all()

    phase_financials = []

    for phase in phases:
        actual_cost = db.session.scalar(
            db.select(
                db.func.coalesce(
                    db.func.sum(Expense.amount),
                    0,
                )
            ).where(
                Expense.phase_id == phase.id
            )
        )

        actual_cost = Decimal(actual_cost)
        allocated_budget = Decimal(phase.allocated_budget)

        remaining_budget = (
            allocated_budget - actual_cost
        )

        if allocated_budget > 0:
            budget_utilization = (
                actual_cost / allocated_budget
            ) * Decimal("100")
        else:
            budget_utilization = Decimal("0")

        budget_variance = (
            allocated_budget - actual_cost
        )

        phase_financials.append(
            {
                "phase_id": phase.id,
                "phase_name": phase.name,
                "allocated_budget": allocated_budget,
                "actual_cost": actual_cost,
                "remaining_budget": remaining_budget,
                "budget_variance": budget_variance,
                "budget_utilization": budget_utilization,
                "completion_percentage": Decimal(
                    phase.completion_percentage
                ),
                "status": phase.status,
                "is_over_budget": actual_cost > allocated_budget,
            }
        )

    return phase_financials


def get_project_progress_summary(project_id):
    project = db.session.get(Project, project_id)

    if project is None:
        raise ValueError("Project not found.")

    phases = db.session.scalars(
        db.select(Phase)
        .where(Phase.project_id == project_id)
        .order_by(Phase.id)
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
            allocated_budget
            * completion_percentage
        )

    if total_allocated_budget > 0:
        overall_progress = (
            weighted_progress
            / total_allocated_budget
        )
    else:
        overall_progress = Decimal("0")

    return {
        "overall_progress": overall_progress,
        "total_phases": len(phases),
        "completed_phases": sum(
            phase.status == "completed"
            for phase in phases
        ),
        "in_progress_phases": sum(
            phase.status == "in_progress"
            for phase in phases
        ),
        "not_started_phases": sum(
            phase.status == "not_started"
            for phase in phases
        ),
        "on_hold_phases": sum(
            phase.status == "on_hold"
            for phase in phases
        ),
    }


def get_project_cost_escalation(project_id):
    project = db.session.get(Project, project_id)

    if project is None:
        raise ValueError("Project not found.")

    expenses = db.session.scalars(
        db.select(Expense)
        .where(
            Expense.project_id == project_id
        )
        .order_by(
            Expense.expense_date.asc(),
            Expense.id.asc(),
        )
    ).all()

    monthly_costs = defaultdict(
        lambda: Decimal("0")
    )

    for expense in expenses:
        month_key = expense.expense_date.strftime(
            "%Y-%m"
        )

        monthly_costs[month_key] += Decimal(
            expense.amount
        )

    cumulative_cost = Decimal("0")
    escalation_data = []

    for month, monthly_cost in sorted(
        monthly_costs.items()
    ):
        cumulative_cost += monthly_cost

        escalation_data.append(
            {
                "month": month,
                "monthly_cost": monthly_cost,
                "cumulative_cost": cumulative_cost,
            }
        )

    return escalation_data
