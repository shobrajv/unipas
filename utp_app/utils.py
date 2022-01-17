import time
import hashlib
import json
import jwt
import logging
import pdfkit
import requests
import qrcode

log = logging.getLogger(__name__)

def generate_sha256(string_value):
    string_value_sha256 = hashlib.sha256(string_value.encode())
    return string_value_sha256.hexdigest()

def generate_otp(phone_number, full_name):
    print(f">> Generating OTP for: {phone_number}")
    # return "*"*36
    url = "https://cdn-api.co-vin.in/api/v2/auth/public/generateOTP"
    header = {
        "Content-Type": "application/json"
    }
    payload = {
        "mobile": str(phone_number),
        # "full_name": full_name
    }
    print(f">> Generating OTP for Mobile Number: {phone_number}")
    result = requests.post(url, data=json.dumps(payload), headers=header)
    print(f">> Generating OTP response status: {result.status_code}")
    print(f">> Generating OTP response text: {result.text}")
    time.sleep(1)
    if result.status_code == 200:
        result_json = result.text.replace("'", "\"")
        result_dict = json.loads(result_json)
        return result_dict["txnId"]
    else:
        return None


def confirm_otp(otp, txnId):
    url = "https://cdn-api.co-vin.in/api/v2/auth/public/confirmOTP"
    header = {
        "Content-Type": "application/json"
    }
    payload = {
        "otp": str(generate_sha256(otp)),
        "txnId": txnId
    }
    print(f">> Confirming OTP: {otp}, txnId: {txnId}")
    result = requests.post(url, data=json.dumps(payload), headers=header)
    print(f">> Confirming OTP response status: {result.status_code}")
    print(f">> Confirming OTP response text: {result.text}")
    result_json = result.text.replace("'", "\"")
    result_dict = json.loads(result_json)
    return result_dict["token"]

def get_beneficiary_reference_id(jwt_token):
    decoded_jwt_token = jwt.decode(jwt=jwt_token, algorithms=['HS256'], options={"verify_signature": False})
    return decoded_jwt_token["beneficiary_reference_id"]

def get_certificate(beneficiary_reference_id):
    url = "https://cdn-api.co-vin.in/api/v2/registration/certificate/public/download"
    header = {
        "Content-Type": "application/json"
    }
    payload = {
        "beneficiary_reference_id": beneficiary_reference_id
    }
    print(f">> Downloading Certificate")
    result = requests.get(url, data=json.dumps(payload), headers=header)
    print(f">> Download response status: {result.status_code}")
    print(f">> Download Status response text: {result.text}")

def get_vaccination_status(jwt_token, txnId, otp, full_name, mobile):
    url = "https://cdn-api.co-vin.in/api/v2/vaccination/status"
    url = "https://cdn-api.co-vin.in/api/v3/vaccination/status"
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jwt_token}"
    }
    payload = {
        txnId: txnId,
        otp: otp,
        full_name: full_name,
        mobile: mobile
    }
    print(f">> Getting Vaccination Status")
    result = requests.get(url, data=json.dumps(payload), headers=header)
    print(f">> Vaccination Status response status: {result.status_code}")
    print(f">> Vaccination Status response text: {result.text}")

def generate_qr_code(path_to_pass, beneficiary_id):
    img = qrcode.make(path_to_pass)
    img.save(f"media/uploads/{beneficiary_id}_qr.png")
