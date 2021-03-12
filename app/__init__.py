import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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


def create_app(configuration):
    app = Flask(__name__)
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

    app.register_blueprint(ussd)

    return app


# paywu_gateway = PaywuGateway(app=app)
