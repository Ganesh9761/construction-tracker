from flask import Flask

from config import Config
from app.extensions import csrf, db, login_manager, migrate


def create_app(config_class=Config):
    app = Flask(
        __name__,
        instance_relative_config=True,
    )

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app.models import (
        AuditLog,
        Expense,
        Phase,
        ProgressUpdate,
        Project,
        User,
    )

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(
            User,
            int(user_id),
        )

    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.phases import phases_bp
    from app.routes.projects import projects_bp
    from app.routes.users import users_bp
    from app.routes.expenses import expenses_bp
    from app.routes.progress import progress_bp
    from app.routes.phase_finance import phase_finance_bp
    from app.routes.phase_analysis import phase_analysis_bp
    from app.routes.audit import audit_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(phases_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(phase_finance_bp)
    app.register_blueprint(phase_analysis_bp)
    app.register_blueprint(audit_bp)

    return app
