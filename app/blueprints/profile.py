from __future__ import annotations

from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from app.api_client import backend_api
from app.decorators import login_required, onboarding_required


bp = Blueprint("profile", __name__)


@bp.route("/profile", methods=["GET", "POST"])
@login_required
@onboarding_required
def index():
    api = backend_api()
    if request.method == "POST":
        api.put(
            "/users/me",
            json_body={
                "notifications": {
                    "analysis_complete": request.form.get("analysis_complete") == "on",
                    "project_reminder": request.form.get("project_reminder") == "on",
                    "product_news": request.form.get("product_news") == "on",
                }
            },
        )
        flash("Profilové preference byly uloženy.", "success")
        return redirect(url_for("profile.index"))
    user = api.get("/users/me")["user"]
    usage = api.get("/users/me/usage")
    tier_labels = {
        "unverified": "Neověřený účet",
        "institutional_free": "Akademický Free",
        "basic": "Basic",
        "pro": "Akademický Pro",
    }
    return render_template("profile/index.html", user=user, usage=usage, tier_label=tier_labels.get(user["tier"], user["tier"]))
