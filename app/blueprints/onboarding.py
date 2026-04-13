from __future__ import annotations

from flask import Blueprint, g, redirect, render_template, request, url_for

from app.api_client import backend_api
from app.decorators import login_required


bp = Blueprint("onboarding", __name__)


@bp.route("/onboarding", methods=["GET", "POST"])
@login_required
def index():
    if g.current_user["role"] != "superadmin" and g.current_user.get("onboarding_done") and request.method == "GET":
        return redirect(url_for("projects.dashboard"))

    api = backend_api()
    faculties = api.get("/faculties")["items"]
    selected_faculty = request.form.get("faculty_id", g.current_user.get("faculty_id", "fm"))
    recommended_steps = api.get(f"/faculties/{selected_faculty}/pipeline-steps")["items"]
    pipeline_map = {faculty["id"]: api.get(f"/faculties/{faculty['id']}/pipeline-steps")["items"] for faculty in faculties}

    if request.method == "POST":
        pipeline_mode = request.form.get("pipeline_mode", "recommended")
        selected_steps = request.form.getlist("step_ids") if pipeline_mode == "custom" else [step["id"] for step in recommended_steps]
        api.put(
            "/users/me",
            json_body={
                "faculty_id": selected_faculty,
                "onboarding_done": True,
                "pipeline_preference": {
                    "mode": pipeline_mode,
                    "step_ids": selected_steps,
                },
            },
        )
        return redirect(url_for("projects.dashboard"))

    return render_template(
        "onboarding/index.html",
        faculties=faculties,
        selected_faculty=selected_faculty,
        recommended_steps=recommended_steps,
        pipeline_map=pipeline_map,
    )
