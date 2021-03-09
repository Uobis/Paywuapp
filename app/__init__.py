import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .ussd import ussd
from .service import PaywuGateway


app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")
app.register_blueprint(ussd)

# db = SQLAlchemy(app)
# from app import models
# from .models import User

# migrate = Migrate(app, db)

paywu_gateway = PaywuGateway(app=app)

# @login_manager.user_loader
# def load_user(id):
#     return User.query.filter_by(id=id).first()
