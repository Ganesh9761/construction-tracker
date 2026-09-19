from datetime import date

import pytest

from app import create_app
from app.extensions import db
from app.models import Expense, Phase, Project, User
from app.services.project_finance_service import (
    get_project_cost_escalation,
)


class TestConfig:
    TESTING = True
    SECRET_KEY = "test-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False


@pytest.fixture
def app():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()

        user = User(
            username="finance_test_user",
            email="finance@example.com",
            role="admin",
            is_active=True,
        )
        user.set_password("test-password")

        db.session.add(user)
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


def create_project():
    user = db.session.scalar(
        db.select(User).where(
            User.username == "finance_test_user"
        )
    )

    project = Project(
        name="Cost Escalation Test Project",
        client_name="Test Client",
        location="Bengaluru, Karnataka",
        start_date=date(2026, 9, 1),
        expected_completion_date=date(2027, 9, 1),
        total_budget=10000000,
        status="active",
        created_by=user.id,
    )

    db.session.add(project)
    db.session.flush()

    phase = Phase(
        project_id=project.id,
        name="Foundation",
        description="Foundation test phase",
        allocated_budget=5000000,
        start_date=date(2026, 9, 1),
        expected_completion_date=date(2026, 12, 31),
        completion_percentage=0,
        status="not_started",
    )

    db.session.add(phase)
    db.session.flush()

    return project, phase, user


def create_expense(
    project,
    phase,
    user,
    expense_date,
    amount,
    description,
):
    expense = Expense(
        project_id=project.id,
        phase_id=phase.id,
        expense_date=expense_date,
        category="materials",
        description=description,
        amount=amount,
        vendor_name="Test Vendor",
        payment_status="paid",
        created_by=user.id,
    )

    db.session.add(expense)


def test_cost_escalation_aggregates_expenses_by_month(app):
    with app.app_context():
        project, phase, user = create_project()

        create_expense(
            project,
            phase,
            user,
            date(2026, 9, 5),
            100000,
            "Concrete purchase",
        )

        create_expense(
            project,
            phase,
            user,
            date(2026, 9, 20),
            150000,
            "Steel purchase",
        )

        create_expense(
            project,
            phase,
            user,
            date(2026, 10, 10),
            200000,
            "Additional materials",
        )

        db.session.commit()

        result = get_project_cost_escalation(
            project.id
        )

        assert len(result) == 2

        assert result[0]["month"] == "2026-09"
        assert result[0]["monthly_cost"] == 250000
        assert result[0]["cumulative_cost"] == 250000

        assert result[1]["month"] == "2026-10"
        assert result[1]["monthly_cost"] == 200000
        assert result[1]["cumulative_cost"] == 450000


def test_cost_escalation_orders_months_chronologically(app):
    with app.app_context():
        project, phase, user = create_project()

        create_expense(
            project,
            phase,
            user,
            date(2026, 11, 10),
            300000,
            "November materials",
        )

        create_expense(
            project,
            phase,
            user,
            date(2026, 9, 10),
            100000,
            "September materials",
        )

        create_expense(
            project,
            phase,
            user,
            date(2026, 10, 10),
            200000,
            "October materials",
        )

        db.session.commit()

        result = get_project_cost_escalation(
            project.id
        )

        assert [item["month"] for item in result] == [
            "2026-09",
            "2026-10",
            "2026-11",
        ]

        assert [
            item["cumulative_cost"]
            for item in result
        ] == [
            100000,
            300000,
            600000,
        ]


def test_cost_escalation_returns_empty_for_project_without_expenses(
    app,
):
    with app.app_context():
        project, _, _ = create_project()

        db.session.commit()

        result = get_project_cost_escalation(
            project.id
        )

        assert result == []


def test_cost_escalation_rejects_missing_project(app):
    with app.app_context():
        with pytest.raises(ValueError, match="Project not found."):
            get_project_cost_escalation(99999)
