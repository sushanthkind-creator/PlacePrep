from app.routes import auth, dashboard, learning, practice, profile, tests


def register_blueprints(app):
    for module in (auth, profile, learning, practice, tests, dashboard):
        app.register_blueprint(module.bp)
