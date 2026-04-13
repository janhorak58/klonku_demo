from __future__ import annotations

import os

from flask import Flask

from app.blueprints import admin, auth, onboarding, profile, projects
from app.decorators import load_current_user


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "klonku-dev-secret")
    app.config["BACKEND_URL"] = os.environ.get("BACKEND_URL", "http://127.0.0.1:5001")

    app.before_request(load_current_user)

    app.register_blueprint(auth.bp)
    app.register_blueprint(onboarding.bp)
    app.register_blueprint(projects.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(admin.bp)

    return app
