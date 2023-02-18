from flask import Flask
from config import Config
from git_app.extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from git_app.views import events as bp
    app.register_blueprint(bp)

    return app
