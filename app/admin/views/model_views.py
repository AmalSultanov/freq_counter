from app.admin.views.base import BaseReadOnlyModelView


class UserModelView(BaseReadOnlyModelView):
    form_columns = ["username", "password", "documents", "collections"]
    column_list = ["id", "username", "documents", "collections", "created_at"]
    column_searchable_list = ["username"]
    column_filters = [
        "username", "password", "documents", "collections", "created_at"
    ]


class DocumentModelView(BaseReadOnlyModelView):
    form_columns = [
        "name", "contents", "content_hash", "user_id", "collections"
    ]
    column_list = ["id", "name", "user_id", "collections", "created_at"]
    column_searchable_list = ["name", "contents", "user_id"]
    column_filters = [
        "name", "contents", "user_id", "collections", "created_at"
    ]


class CollectionModelView(BaseReadOnlyModelView):
    form_columns = ["name", "user_id", "documents"]
    column_list = ["id", "name", "user_id", "documents", "created_at"]
    column_searchable_list = ["name", "user_id"]
    column_filters = ["name", "user_id", "documents", "created_at"]


class DocumentCollectionModelView(BaseReadOnlyModelView):
    column_display_pk = False
    form_columns = ["document_id", "collection_id", "document", "collection"]
    column_list = [
        "document_id", "collection_id", "document", "collection", "created_at"
    ]
    column_searchable_list = ["document_id", "collection_id"]
    column_filters = [
        "document_id", "collection_id", "document", "collection", "created_at"
    ]


class DocumentMetricModelView(BaseReadOnlyModelView):
    form_columns = ["word_count", "size"]
    column_list = ["id", "word_count", "size", "document", "created_at"]
    column_searchable_list = ["word_count", "size"]
    column_filters = ["word_count", "size", "document.name", "created_at"]
