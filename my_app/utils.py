import hmac
import hashlib
import requests
from datetime import datetime
from twilio.rest import Client


def link_thanh_toan(gia, url):
    requestId = "tuyen" + str(int(datetime.now().timestamp()))
    data = "accessKey=RCmyRRu3ONRNC9xm&amount=" + str(int(float(gia))) + "&extraData=&ipnUrl=" + url + "&orderId=" + requestId + "&orderInfo=Thanh toán qua ví MoMo&partnerCode=MOMOFIF820211121&redirectUrl=" + url + "&requestId=" + requestId + "&requestType=captureWallet"
    signature = hmac.new(b"srorZC05FI40gRaEPYCMJjFKDGjtf4BM", data.encode(), hashlib.sha256).hexdigest()
    params = {
        "partnerCode": "MOMOFIF820211121",
        "partnerName": "Tuyen",
        "storeId": "Tuyen",
        "requestType": "captureWallet",
        "ipnUrl": url,
        "redirectUrl": url,
        "orderId": requestId,
        "amount": int(float(gia)),
        "lang": "en",
        "autoCapture": False,
        "orderInfo": "Thanh toán qua ví MoMo",
        "requestId": requestId,
        "extraData": "",
        "signature": signature
    }
    return requests.post(url='https://test-payment.momo.vn/v2/gateway/api/create', json=params,
                  headers={"Content-Type": "application/json; charset=UTF-8"})


def confirm_thanh_toan(gia, requestId):
    data = "accessKey=RCmyRRu3ONRNC9xm&amount=" +  str(int(float(gia))) + "&description=Xac nhan thanh toan&orderId=" + requestId + "&partnerCode=MOMOFIF820211121&requestId=" + requestId +  "&requestType=capture"
    signature = hmac.new(b"srorZC05FI40gRaEPYCMJjFKDGjtf4BM", data.encode(), hashlib.sha256).hexdigest()
    params = {
                "partnerCode": "MOMOFIF820211121",
                "requestId": requestId,
                "orderId": requestId,
                "requestType": "capture",
                "lang": "vi",
                "amount": int(float(gia)),
                "description": "Xac nhan thanh toan",
                "signature": signature
            }
    return requests.post(url='https://test-payment.momo.vn/v2/gateway/api/confirm', json=params,
                         headers={"Content-Type": "application/json; charset=UTF-8"})


def gui_sms(phone, message):
    try:
        client = Client("AC2de7639eaf115bcb2195774eb91a3b6f", "2b33e5f98fda5165051f21edb9645dc1")
        client.messages.create(to="+84" + phone, from_="+14422281058", body=message)
        return {"error_code": 200, "message": "Gửi sms thành công"}
    except Exception as ex:
        return {"error_code": 404, "message": "Gửi sms thất bại"}