from __future__ import annotations

from functools import wraps
from typing import Any

from flask import Flask, g, jsonify, request

from app.state import store


def _json() -> dict[str, Any]:
    return request.get_json(silent=True) or {}


def _serialize_user(user: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in user.items() if key != "password"}


def _serialize_project(project: dict[str, Any]) -> dict[str, Any]:
    return {
        **project,
        "faculty": store.get_faculty(project["faculty_id"]),
    }


def _serialize_version(version: dict[str, Any]) -> dict[str, Any]:
    return dict(version)


def _bearer_token() -> str | None:
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return None
    return header.split(" ", 1)[1].strip()


def _login_response(user: dict[str, Any]):
    tokens = store.issue_tokens(user["id"])
    return jsonify(
        {
            **tokens,
            "user": _serialize_user(user),
        }
    )


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user = store.get_user_by_access_token(_bearer_token())
        if not user:
            return jsonify({"error": "unauthorized"}), 401
        g.api_user = user
        return view(*args, **kwargs)

    return wrapped


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if g.api_user["role"] != "superadmin":
            return jsonify({"error": "forbidden"}), 403
        return view(*args, **kwargs)

    return wrapped


def _project_for_user(project_id: str) -> dict[str, Any] | None:
    user_id = None if g.api_user["role"] == "superadmin" else g.api_user["id"]
    return store.get_project(project_id, user_id)


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.post("/auth/register")
    def register():
        payload = _json()
        user, error = store.register_user(payload.get("email", "").strip(), payload.get("password", "").strip())
        if error:
            return jsonify({"error": error}), 400
        verification_token = store.create_email_verification_token(user["id"])
        return jsonify({"user": _serialize_user(user), "verification_token": verification_token}), 201

    @app.post("/auth/login")
    def login():
        payload = _json()
        user, error = store.authenticate(payload.get("email", "").strip(), payload.get("password", "").strip())
        if error:
            return jsonify({"error": error}), 400
        if not user["email_verified"]:
            return (
                jsonify(
                    {
                        "error": "email_not_verified",
                        "verification_token": store.create_email_verification_token(user["id"]),
                        "user": _serialize_user(user),
                    }
                ),
                403,
            )
        return _login_response(user)

    @app.post("/auth/google")
    def google():
        user = store.get_user("user-jan")
        return _login_response(user)

    @app.post("/auth/refresh")
    def refresh():
        payload = _json()
        tokens = store.refresh_tokens(payload.get("refresh_token"))
        if not tokens:
            return jsonify({"error": "invalid_refresh_token"}), 401
        return jsonify(tokens)

    @app.post("/auth/logout")
    def logout():
        payload = _json()
        store.revoke_session(payload.get("refresh_token"))
        return ("", 204)

    @app.get("/auth/verify-email/<token>")
    def verify_email(token: str):
        user = store.verify_email_token(token)
        if not user:
            return jsonify({"error": "invalid_verification_token"}), 404
        return _login_response(user)

    @app.post("/auth/forgot-password")
    def forgot_password():
        payload = _json()
        token = store.create_password_reset_token(payload.get("email", "").strip())
        return jsonify({"status": "accepted", "reset_token": token})

    @app.post("/auth/reset-password")
    def reset_password():
        payload = _json()
        user = store.reset_password(payload.get("token", ""), payload.get("password", "").strip())
        if not user:
            return jsonify({"error": "invalid_reset_token"}), 404
        return jsonify({"status": "password_updated"})

    @app.get("/users/me")
    @login_required
    def me():
        return jsonify({"user": _serialize_user(g.api_user)})

    @app.put("/users/me")
    @login_required
    def update_me():
        payload = _json()
        user = store.update_profile(
            g.api_user["id"],
            first_name=payload.get("first_name"),
            last_name=payload.get("last_name"),
            faculty_id=payload.get("faculty_id"),
            onboarding_done=payload.get("onboarding_done"),
            pipeline_preference=payload.get("pipeline_preference"),
            notifications=payload.get("notifications"),
        )
        return jsonify({"user": _serialize_user(user)})

    @app.get("/users/me/usage")
    @login_required
    def usage():
        return jsonify(store.get_usage(g.api_user["id"]))

    @app.get("/projects")
    @login_required
    def projects():
        return jsonify({"items": store.list_projects_for_user(g.api_user["id"])})

    @app.post("/projects")
    @login_required
    def create_project():
        payload = _json()
        project = store.create_project(
            g.api_user["id"],
            payload.get("title", "").strip(),
            payload.get("faculty_id", "fm"),
            payload.get("file_format", "DOCX"),
            payload.get("thesis_type", "Bakalářská práce"),
            payload.get("pipeline_step_ids", []),
        )
        return jsonify({"project": _serialize_project(project)}), 201

    @app.get("/projects/<project_id>")
    @login_required
    def get_project(project_id: str):
        project = _project_for_user(project_id)
        if not project:
            return jsonify({"error": "not_found"}), 404
        return jsonify({"project": _serialize_project(project)})

    @app.put("/projects/<project_id>")
    @login_required
    def update_project(project_id: str):
        project = _project_for_user(project_id)
        if not project:
            return jsonify({"error": "not_found"}), 404
        payload = _json()
        project = store.update_project(
            project_id,
            title=payload.get("title"),
            faculty_id=payload.get("faculty_id"),
            file_format=payload.get("file_format"),
            thesis_type=payload.get("thesis_type"),
        )
        return jsonify({"project": _serialize_project(project)})

    @app.delete("/projects/<project_id>")
    @login_required
    def delete_project(project_id: str):
        project = _project_for_user(project_id)
        if not project:
            return jsonify({"error": "not_found"}), 404
        store.delete_project(project_id)
        return ("", 204)

    @app.get("/projects/<project_id>/pipeline-config")
    @login_required
    def get_project_pipeline(project_id: str):
        project = _project_for_user(project_id)
        if not project:
            return jsonify({"error": "not_found"}), 404
        return jsonify(store.get_project_pipeline_config(project_id))

    @app.put("/projects/<project_id>/pipeline-config")
    @login_required
    def update_project_pipeline(project_id: str):
        project = _project_for_user(project_id)
        if not project:
            return jsonify({"error": "not_found"}), 404
        payload = _json()
        store.update_project_pipeline(project_id, payload.get("step_ids", []))
        return jsonify(store.get_project_pipeline_config(project_id))

    @app.get("/projects/<project_id>/versions")
    @login_required
    def versions(project_id: str):
        project = _project_for_user(project_id)
        if not project:
            return jsonify({"error": "not_found"}), 404
        return jsonify({"items": [_serialize_version(item) for item in store.get_versions_for_project(project_id)]})

    @app.post("/projects/<project_id>/versions")
    @login_required
    def create_version(project_id: str):
        project = _project_for_user(project_id)
        if not project:
            return jsonify({"error": "not_found"}), 404
        payload = _json()
        version = store.create_version(project_id, payload.get("filename", "nova-verze.docx"))
        return jsonify({"version": _serialize_version(version)}), 201

    @app.get("/projects/<project_id>/versions/<version_id>")
    @login_required
    def get_version(project_id: str, version_id: str):
        project = _project_for_user(project_id)
        version = store.get_version(project_id, version_id)
        if not project or not version:
            return jsonify({"error": "not_found"}), 404
        return jsonify({"version": _serialize_version(version)})

    @app.get("/projects/<project_id>/versions/<version_id>/document")
    @login_required
    def get_document(project_id: str, version_id: str):
        project = _project_for_user(project_id)
        version = store.get_version(project_id, version_id)
        if not project or not version:
            return jsonify({"error": "not_found"}), 404
        return jsonify({"html": store.get_version_document(version_id)})

    @app.get("/projects/<project_id>/versions/<version_id>/errors")
    @login_required
    def get_errors(project_id: str, version_id: str):
        project = _project_for_user(project_id)
        version = store.get_version(project_id, version_id)
        if not project or not version:
            return jsonify({"error": "not_found"}), 404
        return jsonify({"items": store.get_version_errors(version_id)})

    @app.get("/projects/<project_id>/versions/<version_id>/diff")
    @login_required
    def get_diff(project_id: str, version_id: str):
        project = _project_for_user(project_id)
        version = store.get_version(project_id, version_id)
        diff = store.get_diff(version_id)
        if not project or not version or not diff:
            return jsonify({"error": "not_found"}), 404
        return jsonify({"diff": diff})

    @app.delete("/projects/<project_id>/versions/<version_id>")
    @login_required
    def delete_version(project_id: str, version_id: str):
        project = _project_for_user(project_id)
        version = store.get_version(project_id, version_id)
        if not project or not version:
            return jsonify({"error": "not_found"}), 404
        store.delete_version(project_id, version_id)
        return ("", 204)

    @app.get("/projects/<project_id>/versions/<version_id>/analysis")
    @login_required
    def analysis(project_id: str, version_id: str):
        project = _project_for_user(project_id)
        version = store.get_version(project_id, version_id)
        if not project or not version:
            return jsonify({"error": "not_found"}), 404
        return jsonify(store.get_analysis_status(project_id, version_id))

    @app.post("/projects/<project_id>/versions/<version_id>/analysis/retry")
    @login_required
    def retry_analysis(project_id: str, version_id: str):
        project = _project_for_user(project_id)
        version = store.get_version(project_id, version_id)
        if not project or not version:
            return jsonify({"error": "not_found"}), 404
        store.retry_analysis(project_id, version_id)
        return jsonify({"status": "processing"})

    @app.get("/faculties/<faculty_id>/pipeline-steps")
    @login_required
    def faculty_steps(faculty_id: str):
        faculty = store.get_faculty(faculty_id)
        if not faculty:
            return jsonify({"error": "not_found"}), 404
        return jsonify({"items": store.get_pipeline_steps(faculty_id)})

    @app.get("/faculties")
    @login_required
    def faculties():
        return jsonify({"items": store.list_faculties()})

    @app.get("/errors/<error_id>")
    @login_required
    def error_detail(error_id: str):
        user_id = None if g.api_user["role"] == "superadmin" else g.api_user["id"]
        error = store.get_error(error_id, user_id=user_id)
        if not error:
            return jsonify({"error": "not_found"}), 404
        return jsonify({"error": error})

    @app.get("/error-types")
    @login_required
    def error_types():
        return jsonify({"items": store.list_error_types()})

    @app.get("/admin")
    @admin_required
    def admin_overview():
        return jsonify(store.get_admin_overview())

    @app.get("/admin/users")
    @admin_required
    def admin_users():
        return jsonify({"items": [_serialize_user(user) for user in store.list_admin_users()]})

    @app.get("/admin/users/<user_id>")
    @admin_required
    def admin_user_detail(user_id: str):
        user = store.get_user(user_id)
        if not user:
            return jsonify({"error": "not_found"}), 404
        return jsonify({"user": _serialize_user(user), "usage": store.get_usage(user_id)})

    @app.put("/admin/users/<user_id>")
    @admin_required
    def admin_user_update(user_id: str):
        if not store.get_user(user_id):
            return jsonify({"error": "not_found"}), 404
        payload = _json()
        store.update_user(
            user_id,
            payload.get("role", "student"),
            payload.get("tier", "institutional_free"),
            int(payload.get("monthly_scan_budget", 0)),
        )
        return jsonify({"user": _serialize_user(store.get_user(user_id))})

    @app.delete("/admin/users/<user_id>")
    @admin_required
    def admin_user_delete(user_id: str):
        if not store.get_user(user_id):
            return jsonify({"error": "not_found"}), 404
        store.delete_user(user_id)
        return ("", 204)

    @app.get("/admin/faculties")
    @admin_required
    def admin_faculties():
        items = []
        for faculty in store.list_faculties():
            items.append({**faculty, "pipeline_count": len(store.get_pipeline_steps(faculty["id"]))})
        return jsonify({"items": items})

    @app.post("/admin/faculties")
    @admin_required
    def admin_faculty_create():
        payload = _json()
        faculty = store.create_faculty(
            payload.get("code", "").strip(),
            payload.get("name", "").strip(),
            payload.get("short_name", "").strip(),
            payload.get("university_name", "").strip(),
        )
        return jsonify({"faculty": faculty}), 201

    @app.get("/admin/faculties/<faculty_id>/pipeline-steps")
    @admin_required
    def admin_faculty_pipeline(faculty_id: str):
        faculty = store.get_faculty(faculty_id)
        if not faculty:
            return jsonify({"error": "not_found"}), 404
        return jsonify({"faculty": faculty, "items": store.get_pipeline_steps(faculty_id)})

    @app.post("/admin/faculties/<faculty_id>/pipeline-steps")
    @admin_required
    def admin_faculty_pipeline_create(faculty_id: str):
        if not store.get_faculty(faculty_id):
            return jsonify({"error": "not_found"}), 404
        payload = _json()
        store.add_pipeline_step(faculty_id, payload.get("name", "").strip(), payload.get("description", "").strip())
        return jsonify({"items": store.get_pipeline_steps(faculty_id)}), 201

    @app.put("/admin/pipeline-steps/<step_id>")
    @admin_required
    def admin_pipeline_step_update(step_id: str):
        if step_id not in store.state["pipeline_steps"]:
            return jsonify({"error": "not_found"}), 404
        payload = _json()
        store.update_pipeline_step(
            step_id,
            name=payload.get("name"),
            description=payload.get("description"),
            active=payload.get("active"),
        )
        return jsonify({"step": store.state["pipeline_steps"][step_id]})

    @app.delete("/admin/pipeline-steps/<step_id>")
    @admin_required
    def admin_pipeline_step_delete(step_id: str):
        if step_id not in store.state["pipeline_steps"]:
            return jsonify({"error": "not_found"}), 404
        store.delete_pipeline_step(step_id)
        return ("", 204)

    @app.get("/admin/error-types")
    @admin_required
    def admin_error_types():
        return jsonify({"items": store.list_error_types()})

    @app.post("/admin/error-types")
    @admin_required
    def admin_error_type_create():
        payload = _json()
        store.add_error_type(payload.get("slug", "").strip(), payload.get("label", "").strip(), payload.get("description", "").strip())
        return jsonify({"items": store.list_error_types()}), 201

    @app.put("/admin/error-types/<type_id>")
    @admin_required
    def admin_error_type_update(type_id: str):
        if type_id not in store.state["error_types"]:
            return jsonify({"error": "not_found"}), 404
        payload = _json()
        store.update_error_type(type_id, payload.get("label", ""), payload.get("description", ""))
        return jsonify({"error_type": store.state["error_types"][type_id]})

    @app.delete("/admin/error-types/<type_id>")
    @admin_required
    def admin_error_type_delete(type_id: str):
        if type_id not in store.state["error_types"]:
            return jsonify({"error": "not_found"}), 404
        store.delete_error_type(type_id)
        return ("", 204)

    @app.get("/admin/allowed-domains")
    @admin_required
    def admin_allowed_domains():
        return jsonify({"items": store.list_allowed_domains()})

    @app.post("/admin/allowed-domains")
    @admin_required
    def admin_allowed_domain_create():
        payload = _json()
        store.add_allowed_domain(
            payload.get("domain", "").strip(),
            payload.get("university_name", "").strip(),
            int(payload.get("free_analyses_per_month", 0)),
        )
        return jsonify({"items": store.list_allowed_domains()}), 201

    @app.patch("/admin/allowed-domains/<domain_id>")
    @admin_required
    def admin_allowed_domain_update(domain_id: str):
        if domain_id not in store.state["allowed_domains"]:
            return jsonify({"error": "not_found"}), 404
        payload = _json()
        store.update_allowed_domain(
            domain_id,
            active=payload.get("active"),
            free_analyses_per_month=payload.get("free_analyses_per_month"),
            university_name=payload.get("university_name"),
        )
        return jsonify({"domain": store.state["allowed_domains"][domain_id]})

    @app.delete("/admin/allowed-domains/<domain_id>")
    @admin_required
    def admin_allowed_domain_delete(domain_id: str):
        if domain_id not in store.state["allowed_domains"]:
            return jsonify({"error": "not_found"}), 404
        store.delete_allowed_domain(domain_id)
        return ("", 204)

    @app.get("/admin/audit-log")
    @admin_required
    def admin_audit_log():
        return jsonify({"items": store.list_audit_log()})

    return app
