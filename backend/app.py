from flask import Flask
from flask_cors import CORS
from backend.config import Config
from backend.database import init_db
from backend.routes.objects import bp_objects
from backend.routes.assessments import bp_assessments
from backend.routes.analytics import bp_analytics


def create_app(test_config: dict | None = None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config is not None:
        app.config.update(test_config)

    init_db(app)

    app.register_blueprint(bp_objects)
    app.register_blueprint(bp_assessments)
    app.register_blueprint(bp_analytics)

    @app.get("/api/health")
    def health_check():
        return {"status": "ok"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
