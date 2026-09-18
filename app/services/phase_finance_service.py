from decimal import Decimal

from app.extensions import db
from app.models import Expense, Phase


def get_phase_financial_summary(phase_id):
    phase = db.session.get(Phase, phase_id)

    if phase is None:
        raise ValueError("Phase not found.")

    actual_cost = db.session.scalar(
        db.select(
            db.func.coalesce(
                db.func.sum(Expense.amount),
                0,
            )
        ).where(
            Expense.phase_id == phase_id
        )
    )

    actual_cost = Decimal(actual_cost)
    allocated_budget = Decimal(phase.allocated_budget)

    remaining_budget = allocated_budget - actual_cost

    if allocated_budget > 0:
        budget_utilization = (
            actual_cost / allocated_budget
        ) * Decimal("100")
    else:
        budget_utilization = Decimal("0")

    budget_variance = allocated_budget - actual_cost

    return {
        "allocated_budget": allocated_budget,
        "actual_cost": actual_cost,
        "remaining_budget": remaining_budget,
        "budget_variance": budget_variance,
        "budget_utilization": budget_utilization,
        "is_over_budget": actual_cost > allocated_budget,
    }
