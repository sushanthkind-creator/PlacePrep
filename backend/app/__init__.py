import logging
import secrets

import click
from flask import Flask, jsonify

from app.config import INSTANCE_DIR, Config
from app.extensions import cors, db, jwt, migrate

logger = logging.getLogger(__name__)


def create_app(config_class=Config):
    app = Flask(__name__, instance_path=str(INSTANCE_DIR))
    app.config.from_object(config_class)
    _ensure_secrets(app)

    db.init_app(app)
    # Batch mode lets Alembic alter SQLite tables.
    migrate.init_app(app, db, render_as_batch=True)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    # Import models so SQLAlchemy and Alembic see every table.
    from app import models  # noqa: F401
    from app.routes import register_blueprints
    from app.utils.errors import register_error_handlers
    from app.utils.jwt_handlers import register_jwt_handlers

    register_blueprints(app)
    register_error_handlers(app)
    register_jwt_handlers(jwt)
    _register_cli(app)

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    return app


def _ensure_secrets(app):
    """Use temporary random secrets in development when none are configured, rather than a hardcoded default."""
    for key in ("SECRET_KEY", "JWT_SECRET_KEY"):
        if not app.config.get(key):
            app.config[key] = secrets.token_hex(32)
            logger.warning(
                "%s is not set. Using a temporary random key: everyone is logged out when the server restarts. "
                "Copy backend/.env.example to backend/.env and set your own keys.",
                key,
            )


def _register_cli(app):
    @app.cli.command("seed")
    def seed_command():
        """Insert or update the learning content. Safe to run repeatedly."""
        from app.seed import run_seed

        summary = run_seed()
        click.echo(
            "Seed complete: {sections} sections, {topics} topics, {questions} questions, {tests} tests.".format(**summary)
        )

    @app.cli.command("init-db")
    def init_db_command():
        """Create all tables directly (without migrations) and seed. Handy for a quick demo."""
        from app.seed import run_seed

        db.create_all()
        summary = run_seed()
        click.echo("Database ready: {topics} topics, {questions} questions.".format(**summary))
