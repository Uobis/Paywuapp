import africastalking


class PaywuGateway:
    def __init__(self):
        self.user_name = app.config["AFRI_TALK_USER"]
        self.api_key = app.config["AFRI_TALK_KEY"]

    def send_sms(self, message, phonenumber):
        sms = africastalking.SMSService(username=self.user_name, api_key=self.api_key)

        response = sms.send(message=message, recipients=[phonenumber], sender_id=None)
        print(response)
