from decimal import Decimal

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


def update_expense(
    expense_id,
    project_id,
    phase_id,
    expense_date,
    category,
    description,
    amount,
    vendor_name,
    payment_status,
):
    category = category.strip().lower()
    description = description.strip()
    vendor_name = vendor_name.strip()

    expense = db.session.get(Expense, expense_id)

    if expense is None:
        raise ValueError("Expense not found.")

    if expense.project_id != project_id:
        raise ValueError(
            "Expense does not belong to the selected project."
        )

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

    phase = db.session.get(Phase, phase_id)

    if phase is None:
        raise ValueError("Phase not found.")

    if phase.project_id != project_id:
        raise ValueError(
            "Selected phase does not belong to the selected project."
        )

    expense.phase_id = phase_id
    expense.expense_date = expense_date
    expense.category = category
    expense.description = description
    expense.amount = amount
    expense.vendor_name = vendor_name
    expense.payment_status = payment_status

    db.session.commit()

    return expense


def delete_expense(expense_id, project_id):
    expense = db.session.get(Expense, expense_id)

    if expense is None:
        raise ValueError("Expense not found.")

    if expense.project_id != project_id:
        raise ValueError(
            "Expense does not belong to the selected project."
        )

    db.session.delete(expense)
    db.session.commit()

    return True


def get_expense_category_summary(project_id):
    project = db.session.get(Project, project_id)

    if project is None:
        raise ValueError("Project not found.")

    category_totals = {
        category: Decimal("0")
        for category in sorted(EXPENSE_CATEGORIES)
    }

    rows = db.session.execute(
        db.select(
            Expense.category,
            db.func.sum(Expense.amount),
        )
        .where(
            Expense.project_id == project_id
        )
        .group_by(
            Expense.category
        )
        .order_by(
            Expense.category
        )
    ).all()

    for category, total in rows:
        category_totals[category] = Decimal(total)

    return category_totals


def get_monthly_expense_summary(project_id):
    project = db.session.get(Project, project_id)

    if project is None:
        raise ValueError("Project not found.")

    month_expression = db.func.strftime(
        "%Y-%m",
        Expense.expense_date,
    )

    rows = db.session.execute(
        db.select(
            month_expression.label("month"),
            db.func.sum(Expense.amount).label("total"),
        )
        .where(
            Expense.project_id == project_id
        )
        .group_by(
            month_expression
        )
        .order_by(
            month_expression
        )
    ).all()

    monthly_expenses = []

    for month, total in rows:
        monthly_expenses.append(
            {
                "month": month,
                "total": Decimal(total),
            }
        )

    return monthly_expenses
