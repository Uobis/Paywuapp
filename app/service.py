import africastalking


class PaywuGateway:
    def __init__(self, config):
        user_name = config.AFRI_TALK_USER
        api_key = config.AFRI_TALK_KEY

        self.sms = africastalking.SMSService(username=user_name, api_key=api_key)

    def send(self, message, recipient):
        response = self.sms.send(
            message=message, recipients=[recipient], sender_id=None
        )

        return response

    def send_sms(self, message, recipient):
        response = self.send(message=message, recipient=recipient, sender_id=None)

        return response

    def send_otp(self, recipient, otp):
        response = self.send("PaywuOTP", recipient=recipient, message=f"OTP code {otp}")

        return response