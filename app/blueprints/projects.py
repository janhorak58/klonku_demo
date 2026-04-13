from __future__ import annotations

from copy import deepcopy

from flask import Blueprint, Response, flash, g, jsonify, redirect, render_template, request, url_for

from app.api_client import ApiError, backend_api
from app.decorators import login_required, onboarding_required
from app.state import store


bp = Blueprint("projects", __name__)


def _visible_errors(version_id: str, errors: list[dict[str, str]]) -> tuple[list[dict[str, str]], int]:
    if g.current_user["tier"] == "institutional_free":
        visible = errors[:3]
        return visible, max(0, len(errors) - len(visible))
    return errors, 0


def _demo_payload() -> dict[str, object]:
    project_id = "proj-sentiment"
    version_id = "ver-sentiment-3"
    project = store.get_project(project_id)
    version = store.get_version(project_id, version_id)
    pipeline_config = store.get_project_pipeline_config(project_id)
    all_errors = [deepcopy(item) for item in store.get_version_errors(version_id)]
    category_order = [
        "Chybějící části",
        "Citace a zdroje",
        "Typografie",
        "Jazyk a pravopis",
        "Data a metodika",
    ]
    for index, error in enumerate(all_errors):
        error["reveal_order"] = index

    grouped_errors = []
    for category in category_order:
        items = [error for error in all_errors if error.get("category") == category]
        if items:
            grouped_errors.append({"title": category, "items": items})

    pipeline_steps = [step for step in pipeline_config["steps"] if step["id"] in pipeline_config["step_ids"]]
    return {
        "project": project,
        "version": version,
        "document_html": store.get_version_document(version_id),
        "all_errors": all_errors,
        "grouped_errors": grouped_errors,
        "pipeline_steps": pipeline_steps,
    }


@bp.get("/")
def index():
    if g.current_user:
        if g.current_user["role"] == "superadmin":
            return redirect(url_for("admin.overview"))
        return redirect(url_for("projects.dashboard"))
    return redirect(url_for("auth.login"))


@bp.get("/demo")
def demo():
    return render_template("projects/demo.html", **_demo_payload())


@bp.route("/dashboard", methods=["GET", "POST"])
@login_required
@onboarding_required
def dashboard():
    api = backend_api()
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        faculty_id = request.form.get("faculty_id", "fm")
        file_format = request.form.get("file_format", "DOCX")
        thesis_type = request.form.get("thesis_type", "Bakalářská práce")
        pipeline_mode = request.form.get("pipeline_mode", "recommended")
        selected_steps = request.form.getlist("pipeline_step_ids")
        if not title:
            flash("Název projektu je povinný.", "error")
        else:
            step_payload = selected_steps
            if pipeline_mode == "recommended":
                step_payload = [step["id"] for step in api.get(f"/faculties/{faculty_id}/pipeline-steps")["items"]]
            payload = api.post(
                "/projects",
                json_body={
                    "title": title,
                    "faculty_id": faculty_id,
                    "file_format": file_format,
                    "thesis_type": thesis_type,
                    "pipeline_step_ids": step_payload,
                },
            )
            flash("Projekt byl vytvořen.", "success")
            return redirect(url_for("projects.project_detail", project_id=payload["project"]["id"]))

    faculties = api.get("/faculties")["items"]
    pipeline_map = {faculty["id"]: api.get(f"/faculties/{faculty['id']}/pipeline-steps")["items"] for faculty in faculties}
    projects = api.get("/projects")["items"]
    return render_template("projects/dashboard.html", projects=projects, faculties=faculties, pipeline_map=pipeline_map)


@bp.route("/projects/<project_id>", methods=["GET", "POST"])
@login_required
@onboarding_required
def project_detail(project_id: str):
    api = backend_api()
    try:
        if request.method == "POST":
            action = request.form.get("action")
            if action == "upload_version":
                upload = request.files.get("document")
                filename = upload.filename if upload else ""
                if not upload or not filename:
                    flash("Vyber soubor pro nahrání.", "error")
                elif not filename.lower().endswith((".docx", ".tex")):
                    flash("Povolené jsou jen soubory .docx nebo .tex.", "error")
                else:
                    payload = api.post(f"/projects/{project_id}/versions", json_body={"filename": filename})
                    flash("Nová verze byla nahrána a analýza začala.", "success")
                    return redirect(url_for("projects.analysis", project_id=project_id, version_id=payload["version"]["id"]))
            elif action == "update_pipeline":
                step_ids = request.form.getlist("pipeline_step_ids")
                if step_ids:
                    api.put(f"/projects/{project_id}/pipeline-config", json_body={"step_ids": step_ids})
                    flash("Kontrolní kroky byly upraveny.", "success")
                    return redirect(url_for("projects.project_detail", project_id=project_id))
            elif action == "rename_project":
                title = request.form.get("title", "").strip()
                if title:
                    api.put(f"/projects/{project_id}", json_body={"title": title})
                    flash("Název projektu byl upraven.", "success")
                    return redirect(url_for("projects.project_detail", project_id=project_id))
            elif action == "delete_project":
                api.delete(f"/projects/{project_id}")
                flash("Projekt byl odstraněn.", "success")
                return redirect(url_for("projects.dashboard"))
            elif action == "delete_version":
                version_id = request.form.get("version_id", "")
                if version_id:
                    api.delete(f"/projects/{project_id}/versions/{version_id}")
                    flash("Verze byla odstraněna.", "success")
                    return redirect(url_for("projects.project_detail", project_id=project_id))

        project = api.get(f"/projects/{project_id}")["project"]
        versions = api.get(f"/projects/{project_id}/versions")["items"]
        pipeline_config = api.get(f"/projects/{project_id}/pipeline-config")
    except ApiError:
        return render_template("projects/not_found.html"), 404

    pipeline_steps = [step for step in pipeline_config["steps"] if step["id"] in pipeline_config["step_ids"]]
    return render_template(
        "projects/project_detail.html",
        project=project,
        versions=versions,
        pipeline_steps=pipeline_steps,
        all_steps=pipeline_config["steps"],
        faculty=project["faculty"],
    )


@bp.get("/projects/<project_id>/versions/<version_id>/analysis")
@login_required
@onboarding_required
def analysis(project_id: str, version_id: str):
    api = backend_api()
    try:
        project = api.get(f"/projects/{project_id}")["project"]
        version = api.get(f"/projects/{project_id}/versions/{version_id}")["version"]
    except ApiError:
        return render_template("projects/not_found.html"), 404
    return render_template("projects/analysis.html", project=project, version=version)


@bp.get("/api/analysis-status/<project_id>/<version_id>")
@login_required
def analysis_status(project_id: str, version_id: str) -> Response:
    try:
        payload = backend_api().get(f"/projects/{project_id}/versions/{version_id}/analysis")
    except ApiError as exc:
        return jsonify(exc.payload), exc.status_code
    return jsonify(payload)


@bp.post("/projects/<project_id>/versions/<version_id>/analysis/retry")
@login_required
def analysis_retry(project_id: str, version_id: str):
    try:
        backend_api().post(f"/projects/{project_id}/versions/{version_id}/analysis/retry")
    except ApiError:
        flash("Analýzu se nepodařilo znovu spustit.", "error")
        return redirect(url_for("projects.project_detail", project_id=project_id))
    flash("Analýza byla znovu spuštěna.", "success")
    return redirect(url_for("projects.analysis", project_id=project_id, version_id=version_id))


@bp.get("/projects/<project_id>/versions/<version_id>")
@login_required
@onboarding_required
def results(project_id: str, version_id: str):
    api = backend_api()
    try:
        project = api.get(f"/projects/{project_id}")["project"]
        version = api.get(f"/projects/{project_id}/versions/{version_id}")["version"]
        document_payload = api.get(f"/projects/{project_id}/versions/{version_id}/document")
        error_payload = api.get(f"/projects/{project_id}/versions/{version_id}/errors")
        error_types = api.get("/error-types")["items"]
    except ApiError:
        return render_template("projects/not_found.html"), 404

    all_errors = error_payload["items"]
    visible_errors, hidden_count = _visible_errors(version_id, all_errors)
    return render_template(
        "projects/results.html",
        project=project,
        version=version,
        document_html=document_payload["html"],
        all_errors=all_errors,
        visible_errors=visible_errors,
        hidden_count=hidden_count,
        error_types=error_types,
        user_tier=g.current_user["tier"],
    )


@bp.get("/projects/<project_id>/versions/<version_id>/diff")
@login_required
@onboarding_required
def diff(project_id: str, version_id: str):
    api = backend_api()
    try:
        project = api.get(f"/projects/{project_id}")["project"]
        version = api.get(f"/projects/{project_id}/versions/{version_id}")["version"]
        diff_data = api.get(f"/projects/{project_id}/versions/{version_id}/diff")["diff"]
    except ApiError:
        return render_template("projects/not_found.html"), 404
    return render_template("projects/diff.html", project=project, version=version, diff=diff_data)


@bp.get("/errors/<error_id>")
@login_required
@onboarding_required
def error_detail(error_id: str):
    try:
        error = backend_api().get(f"/errors/{error_id}")["error"]
    except ApiError:
        return render_template("projects/not_found.html"), 404
    return render_template("projects/error_detail.html", error=error)
