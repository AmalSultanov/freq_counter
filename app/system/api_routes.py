from flask import Blueprint, jsonify

from app.system.services import get_uploads_count, get_largest_file
from app.version import __version__

system_api_bp = Blueprint("system_api", __name__)


@system_api_bp.get("/status")
def get_status():
    return jsonify({"status": "OK"}), 200


@system_api_bp.get("/metrics")
def get_metrics():
    return jsonify({
            "uploads_count_per_day": get_uploads_count(),
            "largest_file_size_in_bytes": get_largest_file(),
        })


@system_api_bp.get("/version")
def get_version():
    return jsonify({"version": __version__}), 200
