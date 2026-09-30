import os

from flask import Flask, jsonify

from models.task import db
from routes.tasks import tasks_bp


def create_app():
    app = Flask(__name__)

    database_url = os.getenv(
        "DATABASE_URL",
        "sqlite:///taskflow.db"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(tasks_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "healthy",
            "service": "taskflow-api"
        })

    @app.route("/", methods=["GET"])
    def index():
        return jsonify({
            "application": "TaskFlow",
            "version": "1.0.0",
            "description": "Task management API"
        })

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000))
    )
