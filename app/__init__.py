import os

import africastalking as aft
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object("config.DevelopmentConfig")


# db = SQLAlchemy(app)
# from app import models
# from .models import User

# migrate = Migrate(app, db)
from .service import PaywuGateway
from .urls import urls

# @login_manager.user_loader
# def load_user(id):
#     return User.query.filter_by(id=id).first()
