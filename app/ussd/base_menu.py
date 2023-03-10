from flask import make_response, current_app


class Menu:
    def __init__(self, session_id, user_response, phone_number=None):
        self.session_id = session_id
        self.user_response = user_response
        self.phone_number = phone_number

    def execute(self):
        raise NotImplementedError

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

    # def home(self):
    #     """serves the home menu"""
    #     menu_text = "Input\n".format(self.user.username, current_app.config["APP_NAME"])
    #     menu_text += " 1. Deposit Money\n"
    #     menu_text += " 2. Withdraw Money\n"
    #     menu_text += " 3. Buy Airtime\n"
    #     menu_text += " 4. Check Wallet Balance\n"
    #     self.session["level"] = 1
    #     # print the response on to the page so that our gateway can read it
    #     return self.ussd_proceed(menu_text)