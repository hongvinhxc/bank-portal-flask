import hashlib
import jwt
import os
import functools
import datetime
from flask import request, Response
from bson import json_util
# from flask import request, Response
from ..models.user import User


password = b'123456'

password_hashed = hashlib.sha256(password).hexdigest()

secret_key = os.getenv("SECRET_KEY")

def createDefautlUser():
    if User().count() == 0:
        user = User({
            "username": "admin",
            "password": password_hashed
        })
        user.save()
    
def generateToken(payload):
    payload['exp'] =  datetime.datetime.utcnow() + datetime.timedelta(days=90)
    print(payload, flush=True)
    token = jwt.encode(payload, secret_key, algorithm='HS256').decode('utf-8')
    return token

def identifyToken(token):
    print(token, flush=True)
    payload = jwt.decode(token, secret_key, algorithms=['HS256'])
    return payload

def authMiddleware(func):
    @functools.wraps(func)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return Response(json_util.dumps({ "message": "Invalid token" }), status=401, mimetype='application/json')
        try:
            payload = identifyToken(token)
        except:
            return Response(json_util.dumps({ "message": "Invalid token" }), status=401, mimetype='application/json')
        return func(*args, **kwargs)
    return decorated_function

