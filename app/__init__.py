from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# from flask_mail import Mail
# from flask_login import LoginManager
import africastalking as aft
import os

app = Flask(__name__)

username = "sandbox"
api_key = "3f1bc65b1c29fa85a02c1f99ad4bcc52c1c1c2178aadfbb1d24e8510c94c52e6"
aft.initialize(username, api_key)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app.config["APP_NAME"] = "paywu"
app.config["SECRET_KEY"] = b"\x1c\x92\x07\xc8\xea\xbbA\xa1\x04\xac\xa4I\xc5\x11\x9b\xb1"

app.config["ENV"] = "development"
app.config["DEBUG"] = True
app.config["TESTING"] = False
app.config["DEVELOPMENT"] = True


app.config["CSRF_ENABLED"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgres://paywuadmin:paywu123@localhost:5432/paywu"
    if not app.config["DEBUG"]
    else f'sqlite:///{os.path.join(BASE_DIR, "db.sqlite3")}'
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["CACHE_TYPE"] = "null"


# app.config["MAIL_USE_TLS"] = True
# app.config["MAIL_USE_SSL"] = False
# app.config["MAIL_SERVER"] = "smtp.gmail.com"
# app.config["MAIL_PORT"] = 587
# app.config["MAIL_USERNAME"] = "ndifemike@gmail.com"
# app.config["MAIL_PASSWORD"] = "razyuoksculmzyza"

# app.config["MAIL_DEFAULT_SENDER"] = "ndifemike@gmail.com"


# mail = Mail(app)
# login_manager = LoginManager(app)

# login_manager.login_view = "sign_in"


# db = SQLAlchemy(app)
# from app import models
# from .models import User

# migrate = Migrate(app, db)

from .urls import urls


# @login_manager.user_loader
# def load_user(id):
#     return User.query.filter_by(id=id).first()
