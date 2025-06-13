from flask import session, redirect, url_for, flash
from flask_admin.contrib.sqla import ModelView


class BaseReadOnlyModelView(ModelView):
    column_display_pk = True
    can_create = False
    can_edit = False
    can_delete = False
    can_view_details = True
    can_export = True
    page_size = 50

    def is_accessible(self):
        return session.get("admin_logged_in") is True

    def inaccessible_callback(self, name, **kwargs):
        flash("Please log in as admin", "warning")
        return redirect(url_for("admin_web_bp.login"))
