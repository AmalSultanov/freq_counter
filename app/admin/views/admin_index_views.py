from flask import session, redirect, url_for, flash
from flask_admin import AdminIndexView, expose


class CustomAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not session.get("admin_logged_in"):
            flash("Please log in as admin", "warning")
            return redirect(url_for("admin_web_bp.login"))
        return super().index()
