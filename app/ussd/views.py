from flask import make_response, request

from ..models import USSD_Transactions, db
from . import ussd
from .base_menu import Menu
from .tasks import add_transaction

response = ""


@ussd.route("/", methods=["POST", "GET"])
def index():
    response = make_response("END connection ok")
    response.headers["Content-Type"] = "text/plain"
    return response


@ussd.route("/ussd/callback", methods=["POST", "GET"])
def ussd_callback():
    global response
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")

    text_count = text.count("*")
    # 3698*1000*5858

    # ussd logic
    if text == "":
        # main menu
        response = "CON Welcome to Paywu\n"
        response += "Input Merchant ID:"

    elif text.isdigit():
        response = "CON Input Amount:"
    elif text_count == 1:
        response = "CON Input refCode:"
    elif text_count == 2:
        text = text.split("*")
        merchant_id = text[0]
        amount = text[1]
        refCode = text[2]

        ussd_trans = USSD_Transactions(
            merchant_id=merchant_id,
            amount=amount,
            refCode=refCode,
        )
        db.session.add(ussd_trans)
        db.session.commit()

        add_transaction.apply_async(
            kwargs={"id": ussd_trans.id},
            countdown=900,
        )

        # response = "END Your phone number is {}".format(phone_number)
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
    # elif text == "1*1":
    #     # ussd menus are split using *
    #     account_number = "1243324376742"
    #     response = "END Your account number is {}".format(account_number)
    # elif text == "1*2":
    #     account_balance = "100,000"
    #     response = "END Your account balance is USD {}".format(account_balance)

    print(text)

    return response
