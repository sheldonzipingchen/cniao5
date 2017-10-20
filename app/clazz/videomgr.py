import os
import urllib
import hmac
import hashlib
import base64
import time

def my_urlencode(str):

    reprStr = repr(str).replace(r'\x', '%')
    return reprStr[1:-1]


def create_token(fid, accessKey, secretKey):
    expires = 3600
    deadline = int(time.time()) + expires
    tokenstr = 'id=' + fid + '&deadline=' + str(deadline)
    encodedMsg = base64.b64encode(bytearray(tokenstr,"utf-8"))
    sign = hmac.new(bytearray(secretKey,"utf-8"), msg=encodedMsg,
		digestmod=hashlib.sha1).digest()
    encodedSign  =base64.b64encode(sign)
    token = accessKey + ":" + encodedSign.decode(encoding='utf-8') + ":" + encodedMsg.decode(encoding='utf-8')

    return my_urlencode(token)


def create_by_token(fid, accessKey, secretKey):

    expires = 3600
    deadline = int(time.time()) + expires
    tokenstr = 'id=' + fid + '&deadline=' + str(deadline)
    encodedMsg = base64.b64encode(bytearray(tokenstr,"utf-8"))
    sign = hmac.new(bytearray(secretKey,"utf-8"), msg=encodedMsg,
		digestmod=hashlib.sha1).digest()
    encodedSign  =base64.b64encode(sign)
    token = accessKey + ":" + encodedSign.decode(encoding='utf-8') + ":" + encodedMsg.decode(encoding='utf-8')
    return urllib.quote_plus(token)




def create_player_token(fid):
    access_key =os.environ.get('BAO_FENG_ACCESS_KEY')
    secret_key =os.environ.get('BAO_FENG_SECRET_KEY')

    return create_by_token(fid,access_key,secret_key)