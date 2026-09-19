from functools import wraps

from flask import abort
from flask_login import current_user


ROLE_PERMISSIONS = {
    "admin": {
        "view_dashboard",
        "view_projects",
        "create_project",
        "edit_project",
        "manage_phases",
        "view_expenses",
        "create_expense",
        "edit_expense",
        "delete_expense",
        "update_progress",
        "manage_users",
        "view_financial_analysis",
        "view_audit_logs",
    },
    "project_manager": {
        "view_dashboard",
        "view_projects",
        "create_project",
        "edit_project",
        "manage_phases",
        "view_expenses",
        "create_expense",
        "edit_expense",
        "delete_expense",
        "update_progress",
        "view_financial_analysis",
        "view_audit_logs",
    },
    "site_engineer": {
        "view_dashboard",
        "view_projects",
        "view_expenses",
        "create_expense",
        "update_progress",
        "view_financial_analysis",
    },
}


def has_permission(permission):
    if not current_user.is_authenticated:
        return False

    permissions = ROLE_PERMISSIONS.get(
        current_user.role,
        set(),
    )

    return permission in permissions


def permission_required(permission):
    def decorator(view_function):
        @wraps(view_function)
        def wrapped_view(*args, **kwargs):
            if not has_permission(permission):
                abort(403)

            return view_function(
                *args,
                **kwargs,
            )

        return wrapped_view

    return decorator
