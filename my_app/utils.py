import hmac
import hashlib
import requests
from datetime import datetime

def link_thanh_toan(gia):
    requestId = "tuyen" + str(int(datetime.now().timestamp()))
    data = "accessKey=RCmyRRu3ONRNC9xm&amount=" + str(int(float(gia))) + "&extraData=&ipnUrl=http://127.0.0.1:5000/momo/xu-ly&orderId=" + requestId + "&orderInfo=Thanh toán qua ví MoMo&partnerCode=MOMOFIF820211121&redirectUrl=http://127.0.0.1:5000/momo/xu-ly&requestId=" + requestId + "&requestType=captureWallet"
    signature = hmac.new(b"srorZC05FI40gRaEPYCMJjFKDGjtf4BM", data.encode(), hashlib.sha256).hexdigest()
    params = {
        "partnerCode": "MOMOFIF820211121",
        "partnerName": "Tuyen",
        "storeId": "Tuyen",
        "requestType": "captureWallet",
        "ipnUrl": "http://127.0.0.1:5000/momo/xu-ly",
        "redirectUrl": "http://127.0.0.1:5000/momo/xu-ly",
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