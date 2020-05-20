import jwt
import os
import datetime
import requests
from dotenv import load_dotenv
load_dotenv()

from .models import CustomUser, CustomToken, Organization

def get_object(token):
    try:
        token = token.split(" ")
        payload = jwt.decode(token[1], os.getenv('JWT_SECRET'), algorithms=['HS256'])
        if payload['user_type']==0:
            # General User            
            required_object = CustomUser.objects.get(id=payload['id'])
        else:
            # Organisation
            required_object = Organization.objects.get(id=payload['id'])
            pass
        token = CustomToken.objects.get(object_id=required_object.id, user_type=payload['user_type'])
        return required_object
    except Exception as error:
        print(error)
        return None

def get_token(object_id, user_type):
    payload = {
        'user_type':user_type,
        'id':object_id,
        'time_stamp':str(datetime.datetime.today())
    }
    encoded_jwt = jwt.encode(payload, os.getenv('JWT_SECRET'), algorithm='HS256')
    result = (encoded_jwt.decode("utf-8"))
    return result

def check_user(token):
    try:
        token = token.split(" ")
        payload = jwt.decode(token[1], os.getenv('JWT_SECRET'), algorithms=['HS256'])
        return payload['user_type']
    except Exception as error:
        print(error)
        return None
    
def sendSMS(phone_number, message):
    url = "https://www.fast2sms.com/dev/bulk"

    querystring = {
        "authorization":os.getenv('SMS_API_KEY'),
        "sender_id":"FSTSMS",
        "message":message,
        "language":"english",
        "route":"p",
        "numbers":','.join(phone_number)
    }

    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)
    