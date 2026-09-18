from app.extensions import db
from app.models import Expense, Phase, Project, User
from app.models.expense import EXPENSE_CATEGORIES, PAYMENT_STATUSES


def create_expense(
    project_id,
    phase_id,
    expense_date,
    category,
    description,
    amount,
    vendor_name,
    payment_status,
    created_by,
):
    category = category.strip().lower()
    description = description.strip()
    vendor_name = vendor_name.strip()

    if expense_date is None:
        raise ValueError("Expense date is required.")

    if category not in EXPENSE_CATEGORIES:
        raise ValueError("Invalid expense category.")

    if not description:
        raise ValueError("Expense description is required.")

    if amount is None or amount <= 0:
        raise ValueError("Expense amount must be greater than zero.")

    if not vendor_name:
        raise ValueError("Vendor name is required.")

    if payment_status not in PAYMENT_STATUSES:
        raise ValueError("Invalid payment status.")

    project = db.session.get(Project, project_id)

    if project is None:
        raise ValueError("Project not found.")

    phase = db.session.get(Phase, phase_id)

    if phase is None:
        raise ValueError("Phase not found.")

    if phase.project_id != project_id:
        raise ValueError(
            "Selected phase does not belong to the selected project."
        )

    user = db.session.get(User, created_by)

    if user is None:
        raise ValueError("User not found.")

    expense = Expense(
        project_id=project_id,
        phase_id=phase_id,
        expense_date=expense_date,
        category=category,
        description=description,
        amount=amount,
        vendor_name=vendor_name,
        payment_status=payment_status,
        created_by=created_by,
    )

    db.session.add(expense)
    db.session.commit()

    return expense
