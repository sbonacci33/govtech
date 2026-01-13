import os
from datetime import timedelta

from flask import Flask, render_template


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(days=30)

    @app.route("/")
    def home() -> str:
        return render_template("index.html")

    return app


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "0") == "1"
    create_app().run(debug=debug_mode)
