import json

from flask import make_response, current_app

# from ..database import redis


class Menu(object):
    def __init__(
        self, session_id, session, user, user_response, phone_number=None, level=None
    ):
        self.session = session
        self.session_id = session_id
        self.user = user
        self.user_response = user_response
        self.phone_number = phone_number
        self.level = level

    def ussd_proceed(self, menu_text):
        # redis.set(self.session_id, json.dumps(self.session))
        menu_text = "CON {}".format(menu_text)
        response = make_response(menu_text, 200)
        response.headers["Content-Type"] = "text/plain"
        return response

    def ussd_end(self, menu_text):
        # redis.delete(self.session_id)
        menu_text = "END {}".format(menu_text)
        response = make_response(menu_text, 200)
        response.headers["Content-Type"] = "text/plain"
        return response

    def home(self):
        """serves the home menu"""
        menu_text = f'{current_app.config["APP_NAME"].capitalize()},\n Choose a service\n'.format(
            self.user.username,
        )
        menu_text += " 1. Deposit Money\n"
        menu_text += " 2. Withdraw Money\n"
        self.session["level"] = 1
        # print the response on to the page so that our gateway can read it
        return self.ussd_proceed(menu_text)
