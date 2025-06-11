from flask_restx import Namespace

api = Namespace(
    "Documents",
    description="Operations over documents available for current user"
)
