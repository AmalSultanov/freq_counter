from app import create_app
from app.config import flask_port, flask_debug

app = create_app()

if __name__ == "__main__":
    app.run(port=flask_port, debug=flask_debug)
