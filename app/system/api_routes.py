from flask_restx import Resource

from app.system.namespace import api
from app.system.services import get_uploads_count, get_largest_file
from app.version import __version__


@api.route("/status")
class StatusResource(Resource):
    @api.doc(
        description="Check if the system is running",
        responses={200: "System is up and running"}
    )
    def get(self):
        """System status check"""
        return {"status": "OK"}, 200


@api.route("/metrics")
class MetricsResource(Resource):
    @api.doc(
        description="Retrieve system usage metrics",
        responses={200: "System metrics returned successfully"}
    )
    def get(self):
        """Get system metrics"""
        return {
            "uploads_count_per_day": get_uploads_count(),
            "largest_file_size_in_bytes": get_largest_file(),
        }, 200


@api.route("/version")
class VersionResource(Resource):
    @api.doc(
        description="Get the current version of the system",
        responses={200: "Version returned successfully"}
    )
    def get(self):
        """Get current system version"""
        return {"version": __version__}, 200
