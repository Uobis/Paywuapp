import hashlib
import json
import base64

import requests
from app import config
from flask import make_response, request

# from .. import paywu_gateway
from ..models import USSD_Transactions, db
from . import ussd
from .base_menu import Menu
from .tasks import add_transaction

from Crypto.Cipher import DES3, AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

response = ""


def paywu_req(session_id, payload):
    hash_com = f"{session_id};{config['default'].VULTE_API_SECRET}"
    signature = hashlib.md5(hash_com.encode("utf-8"))
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['default'].VULTE_API_KEY}",
        "Signature": signature.hexdigest(),
    }
    url = f"{config['default'].VULTE_API_URL}/v2/transact"
    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def des3_encrypt(secret_key, data):
    md5Key = hashlib.md5(secret_key.encode("UTF-16LE")).digest()
    md5Key += md5Key[0:8]

    blockSize = DES3.block_size
    padDiff = blockSize - len(data) % blockSize
    padding = chr(padDiff) * padDiff
    cipher = DES3.new(md5Key, DES3.MODE_CBC, get_random_bytes(8))
    data += padding
    encrypted_text = cipher.encrypt(data.encode())
    ciphertext = base64.b64encode(encrypted_text).decode("utf-8")
    return ciphertext


@ussd.route("/", methods=["POST", "GET"])
def index():
    response = make_response("END connection ok")
    response.headers["Content-Type"] = "text/plain"
    return response


@ussd.route("/ussd/events", methods=["POST", "GET"])
def ussd_events():
    global response
    # session_id = request.values.get("sessionId", None)
    # service_code = request.values.get("serviceCode", None)
    # phone_number = request.values.get("phoneNumber", None)
    # text = request.values.get("text", "default")
    # print(request.values)
    response = make_response("END connection ok")
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
        response += "Input Customer Account Number:"
    elif text.isdigit():
        response = "CON Input Amount:"
    elif text_count == 1:
        #     response = "CON Input refCode:"
        # elif text_count == 2:
        # print(text)
        text = text.split("*")
        cus_acc_num = text[0]

        amount = text[1]
        # refCode = text[2]

        payload = json.dumps(
            {
                "request_ref": f"{session_id}",
                "request_type": "collect",
                "auth": {
                    "type": "bank.account",
                    "secure": des3_encrypt(config["default"].SECRET_KEY, cus_acc_num),
                    "auth_provider": "Polaris",
                    "route_mode": None,
                },
                "transaction": {
                    "mock_mode": "Inspect",
                    "transaction_ref": f"{session_id}",
                    "transaction_desc": "A random transaction",
                    "transaction_ref_parent": "",
                    "amount": float(amount),
                    "customer": {
                        "customer_ref": phone_number,
                        "firstname": "Chibuzo",
                        "surname": "",
                        "email": "chibuzo@uobis.com",
                        "mobile_no": phone_number,
                    },
                    "meta": {"a_key": "a_meta_value_1", "b_key": "a_meta_value_2"},
                    "details": None,
                },
            }
        )
        # payload = json.dumps(
        #     {
        #         "request_ref": f"{session_id}",
        #         "request_type": "get_banks",
        #         "auth": {
        #             "type": None,
        #             "secure": None,
        #             "auth_provider": "Polaris",
        #             "route_mode": None,
        #         },
        #         "transaction": {
        #             "mock_mode": "Inspect",
        #             "transaction_ref": f"{session_id}",
        #             "transaction_desc": "A random transaction",
        #             "transaction_ref_parent": None,
        #             "amount": 0,
        #             "customer": {
        #                 "customer_ref": "2348086084762",
        #                 "firstname": "Chibuzo",
        #                 "surname": "",
        #                 "email": "chibuzo@uobis.com",
        #                 "mobile_no": "2348086084762",
        #             },
        #             "meta": {
        #                 "a_key": "a_meta_value_1",
        #                 "b_key": "a_meta_value_2",
        #             },
        #             "details": None,
        #         },
        #     }
        # )

        paywu_req(session_id, payload)

        # ussd_trans = USSD_Transactions(
        #     merchant_id=merchant_id,
        #     amount=amount,
        #     refCode=refCode,
        # )
        # db.session.add(ussd_trans)
        # db.session.commit()

        # add_transaction.apply_async(
        #     args=[ussd_trans.id],
        #     countdown=900,
        # )

        response = "END Transaction Recorded"

    print(text)

    return response


@ussd.route("/sms/callback", methods=["POST", "GET"])
def sms_callback():
    global response
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")

    text_count = text.count("*")

    if text == "":
        # main menu
        response = "CON Welcome to Paywu\n"
        response += "Input Account Number:"

    elif text.isdigit():
        response = "CON Input Phonenumber:"
    elif text_count == 1:
        response = "CON Input Amount:"
    elif text_count == 2:
        text = text.split("*")
        acc_num = text[0]
        phone_num = text[1]
        amount = text[2]

        # req = requests.post(
        #     url="https://paywu.uobis.net/bank/callback",
        #     data={"account_number": acc_num, "phonenumer": phone_num, "amount": amount},
        # )


@ussd.route("/bank/callback", methods=["POST", "GET"])
def bank_callback():
    if request.method == "POST":
        pass
    else:
        pass
