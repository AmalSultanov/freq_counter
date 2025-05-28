from flask import render_template, request, Blueprint

from app.tfidf.services import get_table_data

tfidf_bp = Blueprint("tfidf", __name__, url_prefix="/tfidf")


@tfidf_bp.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")

        if file and file.filename.endswith(".txt"):
            table = get_table_data(file)

            return render_template("table.html", table=table)
    return render_template("index.html")
