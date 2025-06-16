from flask_admin import Admin

from app.admin.views.admin_index_views import CustomAdminIndexView
from app.admin.views.base import BaseReadOnlyModelView
from app.admin.views.model_views import (
    UserModelView, DocumentModelView, CollectionModelView,
    DocumentCollectionModelView, DocumentMetricModelView
)

from app.collections.models import CollectionModel
from app.database import db
from app.documents.models import DocumentModel
from app.shared.common_models import DocumentCollectionModel
from app.system.models import DocumentMetricModel
from app.users.models import UserModel

admin = Admin(
    name="Admin Dashboard",
    template_mode="bootstrap4",
    index_view=CustomAdminIndexView(url="/admin/")
)

admin.add_view(UserModelView(UserModel, db.session))
admin.add_view(DocumentModelView(DocumentModel, db.session))
admin.add_view(CollectionModelView(CollectionModel, db.session))
admin.add_view(DocumentCollectionModelView(
    DocumentCollectionModel, db.session
))
admin.add_view(DocumentMetricModelView(DocumentMetricModel, db.session))
