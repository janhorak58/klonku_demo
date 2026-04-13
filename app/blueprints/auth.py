from __future__ import annotations

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from app.api_client import ApiError, backend_api


bp = Blueprint("auth", __name__)


def _sample_accounts() -> list[dict[str, str]]:
    return [
        {"label": "Student demo", "email": "jan.novak@tul.cz", "password": "demo12345"},
        {"label": "Admin demo", "email": "petra.svobodova@klonku.cz", "password": "admin12345"},
    ]


def _complete_login(payload: dict[str, object]) -> str:
    user = payload["user"]
    session["access_token"] = payload["access_token"]
    session["refresh_token"] = payload["refresh_token"]
    session.pop("pending_verification_token", None)
    session.pop("pending_email", None)
    session.pop("password_reset_token", None)
    if user["role"] != "superadmin" and not user["onboarding_done"]:
        return url_for("onboarding.index")
    if user["role"] == "superadmin":
        return url_for("admin.overview")
    return url_for("projects.dashboard")


@bp.get("/login")
def login():
    if g.current_user:
        if g.current_user["role"] == "superadmin":
            return redirect(url_for("admin.overview"))
        return redirect(url_for("projects.dashboard"))
    return render_template("auth/login.html", sample_accounts=_sample_accounts())


@bp.post("/login")
def login_submit():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()
    api = backend_api()
    try:
        payload = api.post("/auth/login", auth=False, json_body={"email": email, "password": password})
    except ApiError as exc:
        if exc.status_code == 403 and exc.payload.get("error") == "email_not_verified":
            session["pending_verification_token"] = exc.payload["verification_token"]
            session["pending_email"] = exc.payload["user"]["email"]
            flash("Účet čeká na ověření e-mailu. Dokonči ověření a pokračuj do onboardingu.", "warning")
            return redirect(url_for("auth.verify_email"))
        flash(exc.payload.get("error", "Přihlášení se nepodařilo."), "error")
        return render_template("auth/login.html", sample_accounts=_sample_accounts(), form=request.form), 400
    return redirect(_complete_login(payload))


@bp.post("/login/google")
def login_google():
    payload = backend_api().post("/auth/google", auth=False, json_body={"code": "mock-google-code"})
    return redirect(_complete_login(payload))


@bp.get("/register")
def register():
    if g.current_user:
        if g.current_user["role"] == "superadmin":
            return redirect(url_for("admin.overview"))
        return redirect(url_for("projects.dashboard"))
    return render_template("auth/register.html")


@bp.post("/register")
def register_submit():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()
    password_confirm = request.form.get("password_confirm", "").strip()
    if not email or not password:
        flash("Vyplň e-mail i heslo.", "error")
        return render_template("auth/register.html", form=request.form), 400
    if password != password_confirm:
        flash("Hesla se neshodují.", "error")
        return render_template("auth/register.html", form=request.form), 400
    try:
        payload = backend_api().post("/auth/register", auth=False, json_body={"email": email, "password": password})
    except ApiError as exc:
        flash(exc.payload.get("error", "Registrace se nepodařila."), "error")
        return render_template("auth/register.html", form=request.form), 400
    session["pending_verification_token"] = payload["verification_token"]
    session["pending_email"] = payload["user"]["email"]
    return redirect(url_for("auth.verify_email"))


@bp.post("/register/google")
def register_google():
    payload = backend_api().post("/auth/google", auth=False, json_body={"code": "mock-google-code"})
    return redirect(_complete_login(payload))


@bp.get("/verify-email")
def verify_email():
    pending_user = {"email": session.get("pending_email")} if session.get("pending_email") else g.current_user
    return render_template("auth/verify_email.html", pending_user=pending_user)


@bp.post("/verify-email")
def verify_email_submit():
    token = session.get("pending_verification_token")
    if not token:
        flash("Nenalezl jsem účet čekající na ověření.", "warning")
        return redirect(url_for("auth.login"))
    try:
        payload = backend_api().get(f"/auth/verify-email/{token}", auth=False)
    except ApiError:
        flash("Ověřovací odkaz už není platný.", "error")
        return redirect(url_for("auth.login"))
    return redirect(_complete_login(payload))


@bp.get("/forgot-password")
def forgot_password():
    return render_template("auth/forgot_password.html")


@bp.post("/forgot-password")
def forgot_password_submit():
    payload = backend_api().post(
        "/auth/forgot-password",
        auth=False,
        json_body={"email": request.form.get("email", "").strip()},
    )
    session["password_reset_token"] = payload.get("reset_token")
    flash("Pokud účet existuje, poslali jsme na e-mail odkaz pro reset hesla.", "success")
    return render_template("auth/forgot_password.html", submitted=True)


@bp.get("/reset-password")
def reset_password():
    return render_template("auth/reset_password.html")


@bp.post("/reset-password")
def reset_password_submit():
    password = request.form.get("password", "").strip()
    password_confirm = request.form.get("password_confirm", "").strip()
    if not password or password != password_confirm:
        flash("Hesla se neshodují nebo chybí.", "error")
        return render_template("auth/reset_password.html", form=request.form), 400
    token = session.get("password_reset_token")
    if not token:
        flash("Chybí reset token. Začni znovu přes formulář pro zapomenuté heslo.", "error")
        return redirect(url_for("auth.forgot_password"))
    try:
        backend_api().post("/auth/reset-password", auth=False, json_body={"token": token, "password": password})
    except ApiError:
        flash("Reset hesla se nepodařilo dokončit.", "error")
        return render_template("auth/reset_password.html", form=request.form), 400
    session.pop("password_reset_token", None)
    flash("Heslo bylo změněno. Přihlas se novým heslem.", "success")
    return redirect(url_for("auth.login"))


@bp.post("/logout")
def logout():
    refresh_token = session.get("refresh_token")
    if refresh_token:
        try:
            backend_api().post("/auth/logout", auth=False, json_body={"refresh_token": refresh_token})
        except ApiError:
            pass
    session.clear()
    flash("Byl/a jsi odhlášen/a.", "success")
    return redirect(url_for("auth.login"))
