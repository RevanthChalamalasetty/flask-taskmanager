from flask import Flask
from .config import config_map


def create_app(env="development"):
    app = Flask(__name__)
    app.config.from_object(config_map[env])

    from .routes import tasks_bp
    app.register_blueprint(tasks_bp, url_prefix="/api")

    @app.get("/health")
    def health():
        return {"status": "ok", "env": env}

    return app
