from flask import Flask

from app.configs import database, env_configs, migration

from app.routes import leads_blueprint


def create_app():

    app = Flask(__name__)
    env_configs.init_app(app)
    database.init_app(app)
    migration.init_app(app)

    app.register_blueprint(leads_blueprint.bp)

    return app
