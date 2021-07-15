from flask_wtf import FlaskForm
from wtforms import PasswordField, IntegerField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    password = PasswordField("Passcode", validators=[DataRequired()])


class PortalForm(FlaskForm):
    acc_num = IntegerField(
        "Account Number",
        validators=[DataRequired(), Length(min=10, message="Check Account Number")],
    )
