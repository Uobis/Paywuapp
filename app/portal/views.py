from . import portal
from flask import render_template, request, session, redirect, url_for, flash
from flask_login import login_user, current_user, login_required, logout_user
from flask_mail import Message
from .form import LoginForm, PortalForm
from datetime import datetime


@portal.route("/portal", methods=["POST", "GET"])
def portal_home():
    form = LoginForm(request.form)

    return render_template("sign/index.html", form=form, year=datetime.now().year)


@portal.route("/portal/dashboard", methods=["POST", "GET"])
def portal_dashboard():
    form = PortalForm(request.form)
    return render_template("dashboard/index.html", form=form)


@portal.route("/ajax/u", methods=["POST", "GET"])
def ajax_search_user():
    pass


@portal.route("/ajax/u/t", methods=["POST", "GET"])
def ajax_records_table():
    pass