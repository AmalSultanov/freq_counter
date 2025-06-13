from functools import wraps

from flask import session, flash, redirect, url_for


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            flash("Please log in as admin", "warning")

            return redirect(url_for("admin_web_bp.login"))
        return func(*args, **kwargs)
    return wrapper
