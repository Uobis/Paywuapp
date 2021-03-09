from flask import request, make_response
from . import ussd

# from app import paywu_gateway

response = ""


@ussd.route("/", methods=["POST", "GET"])
def index():
    response = make_response("END connection ok")
    response.headers["Content-Type"] = "text/plain"
    return response


@ussd.route("/ussd/callback", methods=["POST", "GET"])
def ussd_callback():
    # sms = paywu_gateway
    global response
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")
    sms_phone_number = []
    sms_phone_number.append(phone_number)

    if not text.find("*") == -1:
        pass
        # text = text.split("*")
        # merchant_id = text[0]
        # amount = text[1]
        # refCode = text[2]

    # ussd logic
    if text == "":
        # main menu
        response = "CON What would you like to do?\n"
        response += "1. Check account details\n"
        response += "2. Check phone number\n"
        response += "3. Send me a cool message"
    elif text == "1":
        # sub menu 1
        response = "CON What would you like to check on your account?\n"
        response += "1. Account number"
        response += "2. Account balance"
    elif text == "2":
        # sub menu 1
        response = "END Your phone number is {}".format(phone_number)
    # elif text == "3":
    #     try:
    #         # sending the sms
    #         sms_response = sms.send_sms(
    #             "Thank you for going through this tutorial", sms_phone_number
    #         )
    #         print(sms_response)
    #     except Exception as e:
    #         # show us what went wrong
    #         print(f"Houston, we have a problem: {e}")
    elif text == "1*1":
        # ussd menus are split using *
        account_number = "1243324376742"
        response = "END Your account number is {}".format(account_number)
    elif text == "1*2":
        account_balance = "100,000"
        response = "END Your account balance is USD {}".format(account_balance)

    print(text)

    return response