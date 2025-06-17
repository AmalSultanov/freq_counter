from flask import (
    Blueprint, request, flash, render_template, redirect, url_for, session
)

from app.admin.decorators import admin_required
from app.admin.services import is_admin_secret_key_valid, register_admin
from app.users.services import (
    get_user_by_username, authenticate_user
)

admin_bp = Blueprint("admin_web_bp", __name__)


@admin_bp.route("/")
@admin_required
def dashboard():
    return render_template("admin/index.html")


@admin_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        admin_secret_key = request.form.get("admin_secret_key")

        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return render_template("admin/register.html")

        if not is_admin_secret_key_valid(admin_secret_key):
            flash("Invalid admin secret key", "danger")
            return render_template("admin/register.html")

        admin = register_admin(username, password)

        if not admin:
            flash("Admin with this username already exists", "danger")
            return render_template("admin/register.html")

        session["admin_logged_in"] = True
        session["admin_username"] = username
        flash("Registration was successful", "success")

        return redirect(url_for("admin_web_bp.dashboard"))
    return render_template("admin/register.html")


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = get_user_by_username(username)

        if user is None:
            flash("User with this username does not exist", "danger")
            return render_template("admin/login.html")

        if not user.check_password(password):
            flash("Invalid password", "danger")
            return render_template("admin/login.html")

        if not user.is_admin:
            flash("You are not authorized, register first", "danger")
            return redirect(url_for("admin_web_bp.register"))

        session["admin_logged_in"] = True
        session["admin_username"] = username
        flash("Login was successful", "success")

        return redirect(url_for("admin_web_bp.dashboard"))
    return render_template("admin/login.html")


@admin_bp.route("/logout")
@admin_required
def logout():
    session.pop("admin_logged_in", None)
    session.pop("admin_username", None)
    flash("Logged out successfully", "success")

    return redirect(url_for("admin_web_bp.login"))
