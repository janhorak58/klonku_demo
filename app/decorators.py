from __future__ import annotations

from functools import wraps

from flask import flash, g, redirect, request, session, url_for

from app.api_client import ApiError, backend_api


def load_current_user() -> None:
    g.current_user = None
    access_token = session.get("access_token")
    refresh_token = session.get("refresh_token")
    if not access_token:
        return
    api = backend_api()
    try:
        payload = api.get("/users/me")
        g.current_user = payload["user"] if payload else None
    except ApiError as exc:
        if exc.status_code == 401 and refresh_token:
            try:
                refresh_payload = api.post("/auth/refresh", auth=False, json_body={"refresh_token": refresh_token})
                session["access_token"] = refresh_payload["access_token"]
                session["refresh_token"] = refresh_payload["refresh_token"]
                payload = api.get("/users/me")
                g.current_user = payload["user"] if payload else None
                return
            except ApiError:
                pass
        session.pop("access_token", None)
        session.pop("refresh_token", None)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not g.current_user:
            flash("Nejprve se přihlas do demo aplikace.", "warning")
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


def onboarding_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not g.current_user:
            return redirect(url_for("auth.login"))
        if g.current_user["role"] != "superadmin" and not g.current_user.get("onboarding_done"):
            return redirect(url_for("onboarding.index"))
        return view(*args, **kwargs)

    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not g.current_user:
            return redirect(url_for("auth.login"))
        if g.current_user["role"] != "superadmin":
            flash("Tato sekce je dostupná jen pro administrátory.", "error")
            return redirect(url_for("projects.dashboard"))
        return view(*args, **kwargs)

    return wrapped
