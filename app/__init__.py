from flask import Flask

from app.config import Config
from app.extensions import db, migrate, login_manager

# Load database models
from app import models

# Blueprint imports
from app.auth.routes import auth_bp
from app.expenses.routes import expense_bp
from app.reports.routes import report_bp
from app.admin.routes import admin_bp

# User model for Flask-Login
from app.models.user import User


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Flask-Login configuration
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    @app.route("/")
    def home():
        return {
            "application": "CloudExpense Pro",
            "status": "running",
            "phase": "Phase 3"
        }

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(expense_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(admin_bp)

    return app

