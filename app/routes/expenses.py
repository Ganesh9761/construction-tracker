from datetime import datetime
from decimal import Decimal, InvalidOperation

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models import Expense, Phase, Project
from app.models.expense import EXPENSE_CATEGORIES, PAYMENT_STATUSES
from app.services.expense_service import (
    create_expense,
    delete_expense,
    update_expense,
)


expenses_bp = Blueprint(
    "expenses",
    __name__,
    url_prefix="/projects/<int:project_id>/expenses",
)


@expenses_bp.route("/")
@login_required
def list_expenses(project_id):
    project = db.session.get(Project, project_id)

    if project is None:
        return "Project not found.", 404

    expenses = db.session.scalars(
        db.select(Expense)
        .where(Expense.project_id == project_id)
        .order_by(
            Expense.expense_date.desc(),
            Expense.id.desc(),
        )
    ).all()

    return render_template(
        "expenses/list.html",
        project=project,
        expenses=expenses,
    )


@expenses_bp.route("/create", methods=["GET", "POST"])
@login_required
def create(project_id):
    project = db.session.get(Project, project_id)

    if project is None:
        return "Project not found.", 404

    phases = db.session.scalars(
        db.select(Phase)
        .where(Phase.project_id == project_id)
        .order_by(Phase.id)
    ).all()

    if request.method == "POST":
        phase_id_text = request.form.get("phase_id", "")
        expense_date_text = request.form.get("expense_date", "")
        category = request.form.get("category", "")
        description = request.form.get("description", "")
        amount_text = request.form.get("amount", "")
        vendor_name = request.form.get("vendor_name", "")
        payment_status = request.form.get(
            "payment_status",
            "pending",
        )

        try:
            phase_id = int(phase_id_text)

            expense_date = datetime.strptime(
                expense_date_text,
                "%Y-%m-%d",
            ).date()

            amount = Decimal(amount_text)

            expense = create_expense(
                project_id=project_id,
                phase_id=phase_id,
                expense_date=expense_date,
                category=category,
                description=description,
                amount=amount,
                vendor_name=vendor_name,
                payment_status=payment_status,
                created_by=current_user.id,
            )

        except (ValueError, InvalidOperation) as error:
            flash(str(error), "error")

            return render_template(
                "expenses/create.html",
                project=project,
                phases=phases,
                categories=sorted(EXPENSE_CATEGORIES),
                payment_statuses=sorted(PAYMENT_STATUSES),
            ), 400

        flash(
            f"Expense #{expense.id} created successfully.",
            "success",
        )

        return redirect(
            url_for(
                "expenses.list_expenses",
                project_id=project_id,
            )
        )

    return render_template(
        "expenses/create.html",
        project=project,
        phases=phases,
        categories=sorted(EXPENSE_CATEGORIES),
        payment_statuses=sorted(PAYMENT_STATUSES),
    )


@expenses_bp.route(
    "/<int:expense_id>/edit",
    methods=["GET", "POST"],
)
@login_required
def edit(expense_id, project_id):
    expense = db.session.get(Expense, expense_id)

    if expense is None:
        return "Expense not found.", 404

    if expense.project_id != project_id:
        return "Expense does not belong to this project.", 403

    project = db.session.get(Project, project_id)

    if project is None:
        return "Project not found.", 404

    phases = db.session.scalars(
        db.select(Phase)
        .where(Phase.project_id == project_id)
        .order_by(Phase.id)
    ).all()

    if request.method == "POST":
        phase_id_text = request.form.get("phase_id", "")
        expense_date_text = request.form.get("expense_date", "")
        category = request.form.get("category", "")
        description = request.form.get("description", "")
        amount_text = request.form.get("amount", "")
        vendor_name = request.form.get("vendor_name", "")
        payment_status = request.form.get(
            "payment_status",
            "pending",
        )

        try:
            phase_id = int(phase_id_text)

            expense_date = datetime.strptime(
                expense_date_text,
                "%Y-%m-%d",
            ).date()

            amount = Decimal(amount_text)

            expense = update_expense(
                expense_id=expense_id,
                project_id=project_id,
                phase_id=phase_id,
                expense_date=expense_date,
                category=category,
                description=description,
                amount=amount,
                vendor_name=vendor_name,
                payment_status=payment_status,
            )

        except (ValueError, InvalidOperation) as error:
            flash(str(error), "error")

            return render_template(
                "expenses/edit.html",
                project=project,
                expense=expense,
                phases=phases,
                categories=sorted(EXPENSE_CATEGORIES),
                payment_statuses=sorted(PAYMENT_STATUSES),
            ), 400

        flash(
            f"Expense #{expense.id} updated successfully.",
            "success",
        )

        return redirect(
            url_for(
                "expenses.list_expenses",
                project_id=project_id,
            )
        )

    return render_template(
        "expenses/edit.html",
        project=project,
        expense=expense,
        phases=phases,
        categories=sorted(EXPENSE_CATEGORIES),
        payment_statuses=sorted(PAYMENT_STATUSES),
    )


@expenses_bp.route(
    "/<int:expense_id>/delete",
    methods=["POST"],
)
@login_required
def delete(expense_id, project_id):
    try:
        delete_expense(
            expense_id=expense_id,
            project_id=project_id,
        )

    except ValueError as error:
        flash(str(error), "error")

        return redirect(
            url_for(
                "expenses.list_expenses",
                project_id=project_id,
            )
        )

    flash(
        f"Expense #{expense_id} deleted successfully.",
        "success",
    )

    return redirect(
        url_for(
            "expenses.list_expenses",
            project_id=project_id,
        )
    )
