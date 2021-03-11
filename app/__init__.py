import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .ussd import ussd
from .service import PaywuGateway
from celery import Celery


app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")
app.register_blueprint(ussd)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

celery = Celery(
    __name__,
    broker=app.config["CELERY_BROKER_URL"],
    backend=app.config["CELERY_RESULT_BACKEND"],
)
celery.conf.update(app.config)

paywu_gateway = PaywuGateway(app=app)

# @login_manager.user_loader
# def load_user(id):
#     return User.query.filter_by(id=id).first()
