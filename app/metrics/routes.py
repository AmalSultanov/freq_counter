from flask import Blueprint, jsonify, redirect

from app.metrics.services import get_uploads_count, get_largest_file
from app.version import __version__

metrics_bp = Blueprint("metrics", __name__)


@metrics_bp.route("/")
def get_homepage():
    return redirect("/tfidf")


@metrics_bp.route("/status")
def get_status():
    return jsonify({"status": "OK"}), 200


@metrics_bp.route("/metrics")
def get_metrics():
    return jsonify(
        {
            "uploads_count_per_day": get_uploads_count(),
            "largest_file_size_in_bytes": get_largest_file(),
        }
    )


@metrics_bp.route("/version")
def get_version():
    return jsonify({"version": __version__}), 200
