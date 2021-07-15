import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_scss import Scss

from .service import PaywuGateway
from config import config, Config


db = SQLAlchemy()


def create_celery():
    from celery import Celery, current_app

    celery = Celery(
        __name__,
        broker=Config.CELERY_BROKER_URL,
        backend=Config.CELERY_RESULT_BACKEND,
    )
    current_app.loader.import_default_modules()
    return celery


celery = create_celery()
celery.autodiscover_tasks(["app.ussd.tasks"], force=True)


def create_gateway(configuration):
    gateway = PaywuGateway(config[configuration])
    return gateway


paywu_gateway = create_gateway("default")


def create_app(configuration):
    app = Flask(__name__, template_folder="./portal/templates")
    app.config.from_object(config[configuration])
    config[configuration].init_app(app)

    db.init_app(app)

    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    from .ussd import ussd
    from .portal import portal

    app.register_blueprint(ussd)
    app.register_blueprint(portal)

    Scss(
        app=app,
        static_dir="app/static/css",
        asset_dir="app/portal/assets/scss",
    )

    return app


# @login_manager.user_loader
# def load_user(id):
# return User.query.filter_by(id=id).first()
