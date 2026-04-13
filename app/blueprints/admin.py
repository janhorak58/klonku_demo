from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.api_client import ApiError, backend_api
from app.decorators import admin_required


bp = Blueprint("admin", __name__)


@bp.get("/admin")
@admin_required
def overview():
    return render_template("admin/overview.html", overview=backend_api().get("/admin"))


@bp.get("/admin/users")
@admin_required
def users():
    return render_template("admin/users.html", users=backend_api().get("/admin/users")["items"])


@bp.route("/admin/users/<user_id>", methods=["GET", "POST"])
@admin_required
def user_detail(user_id: str):
    api = backend_api()
    try:
        if request.method == "POST":
            action = request.form.get("action", "save")
            if action == "delete":
                api.delete(f"/admin/users/{user_id}")
                flash("Uživatel byl odstraněn.", "success")
                return redirect(url_for("admin.users"))
            api.put(
                f"/admin/users/{user_id}",
                json_body={
                    "role": request.form.get("role", "student"),
                    "tier": request.form.get("tier", "institutional_free"),
                    "monthly_scan_budget": int(request.form.get("monthly_scan_budget", 0)),
                },
            )
            flash("Uživatel byl upraven.", "success")
            return redirect(url_for("admin.user_detail", user_id=user_id))
        payload = api.get(f"/admin/users/{user_id}")
    except ApiError:
        flash("Uživatel nebyl nalezen.", "error")
        return redirect(url_for("admin.users"))
    return render_template("admin/user_detail.html", user=payload["user"], usage=payload["usage"])


@bp.route("/admin/faculties", methods=["GET", "POST"])
@admin_required
def faculties():
    api = backend_api()
    if request.method == "POST":
        code = request.form.get("code", "").strip()
        name = request.form.get("name", "").strip()
        short_name = request.form.get("short_name", "").strip()
        university_name = request.form.get("university_name", "").strip()
        if code and name and short_name and university_name:
            api.post(
                "/admin/faculties",
                json_body={
                    "code": code,
                    "name": name,
                    "short_name": short_name,
                    "university_name": university_name,
                },
            )
            flash("Fakulta byla přidána.", "success")
            return redirect(url_for("admin.faculties"))
    return render_template("admin/faculties.html", faculties=api.get("/admin/faculties")["items"])


@bp.route("/admin/faculties/<faculty_id>/pipeline", methods=["GET", "POST"])
@admin_required
def faculty_pipeline(faculty_id: str):
    api = backend_api()
    try:
        if request.method == "POST":
            action = request.form.get("action", "create")
            if action == "create":
                name = request.form.get("name", "").strip()
                description = request.form.get("description", "").strip()
                if name and description:
                    api.post(
                        f"/admin/faculties/{faculty_id}/pipeline-steps",
                        json_body={"name": name, "description": description},
                    )
                    flash("Nový krok pipeline byl přidán.", "success")
            elif action == "update":
                step_id = request.form.get("step_id", "")
                api.put(
                    f"/admin/pipeline-steps/{step_id}",
                    json_body={
                        "name": request.form.get("step_name"),
                        "description": request.form.get("step_description"),
                        "active": request.form.get("active") == "on",
                    },
                )
                flash("Krok pipeline byl upraven.", "success")
            elif action == "delete":
                api.delete(f"/admin/pipeline-steps/{request.form.get('step_id', '')}")
                flash("Krok pipeline byl odstraněn.", "success")
            return redirect(url_for("admin.faculty_pipeline", faculty_id=faculty_id))
        payload = api.get(f"/admin/faculties/{faculty_id}/pipeline-steps")
    except ApiError:
        flash("Fakulta nebyla nalezena.", "error")
        return redirect(url_for("admin.faculties"))
    return render_template("admin/faculty_pipeline.html", faculty=payload["faculty"], steps=payload["items"])


@bp.route("/admin/error-types", methods=["GET", "POST"])
@admin_required
def error_types():
    api = backend_api()
    if request.method == "POST":
        action = request.form.get("action", "create")
        if action == "create":
            slug = request.form.get("slug", "").strip()
            label = request.form.get("label", "").strip()
            description = request.form.get("description", "").strip()
            if slug and label:
                api.post("/admin/error-types", json_body={"slug": slug, "label": label, "description": description})
                flash("Typ chyby byl přidán.", "success")
        elif action == "update":
            type_id = request.form.get("type_id", "")
            api.put(
                f"/admin/error-types/{type_id}",
                json_body={"label": request.form.get("type_label", ""), "description": request.form.get("type_description", "")},
            )
            flash("Typ chyby byl upraven.", "success")
        elif action == "delete":
            api.delete(f"/admin/error-types/{request.form.get('type_id', '')}")
            flash("Typ chyby byl odstraněn.", "success")
        return redirect(url_for("admin.error_types"))
    return render_template("admin/error_types.html", error_types=api.get("/admin/error-types")["items"])


@bp.route("/admin/allowed-domains", methods=["GET", "POST"])
@admin_required
def allowed_domains():
    api = backend_api()
    if request.method == "POST":
        action = request.form.get("action", "create")
        if action == "create":
            domain = request.form.get("domain", "").strip()
            university_name = request.form.get("university_name", "").strip()
            free_analyses_per_month = int(request.form.get("free_analyses_per_month", 1))
            if domain and university_name:
                api.post(
                    "/admin/allowed-domains",
                    json_body={
                        "domain": domain,
                        "university_name": university_name,
                        "free_analyses_per_month": free_analyses_per_month,
                    },
                )
                flash("Doména byla přidána.", "success")
        elif action == "toggle":
            api.patch(
                f"/admin/allowed-domains/{request.form['domain_id']}",
                json_body={"active": request.form.get("current_active") != "true"},
            )
            flash("Stav domény byl změněn.", "success")
        elif action == "update":
            api.patch(
                f"/admin/allowed-domains/{request.form['domain_id']}",
                json_body={
                    "university_name": request.form.get("university_name", ""),
                    "free_analyses_per_month": int(request.form.get("free_analyses_per_month", 0)),
                },
            )
            flash("Doména byla upravena.", "success")
        elif action == "delete":
            api.delete(f"/admin/allowed-domains/{request.form['domain_id']}")
            flash("Doména byla odstraněna.", "success")
        return redirect(url_for("admin.allowed_domains"))
    return render_template("admin/allowed_domains.html", domains=api.get("/admin/allowed-domains")["items"])


@bp.get("/admin/audit-log")
@admin_required
def audit_log():
    return render_template("admin/audit_log.html", entries=backend_api().get("/admin/audit-log")["items"])
