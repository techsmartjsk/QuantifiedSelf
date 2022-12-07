from functools import wraps
from flask import request
import jwt
from QSApp.exceptions import AuthError
from flask import current_app as app

def auth_required(f):
    @wraps(f)
    def check_token(*args, **kwargs):
        token=request.headers.get("Authorization")
        if not(token):
            raise AuthError("Authorization header not present or method not allowed.", "UNAUTH")
        parts=token.split(" ")
        if len(parts)==2:
            my_jwt=parts[1]
        elif len(parts)==1:
            my_jwt=parts[0]
        else:
            raise AuthError("Token format not valid", "UNAUTH")
        try:
            decoded=jwt.decode(my_jwt,"QS App", algorithms=["HS256"])
        except jwt.ExpiredSignatureError as expired:
            raise AuthError("session expired", "SESEXP")
        except:
            raise AuthError("Invalid token or token expired", "UNAUTH")
        if decoded:
            return f(*args, **kwargs)
    return check_token

def get_username_with_token():
    token=request.headers.get("Authorization")
    if not(token):
        raise AuthError("Authorization header not present.", "UNAUTH")
    parts=token.split(" ")
    if len(parts)==2:
        my_jwt=parts[1]
    elif len(parts)==1:
        my_jwt=parts[0]
    else:
        raise AuthError("Token format not valid", "UNAUTH")
    try:
        decoded=jwt.decode(my_jwt,"QS App", algorithms=["HS256"])
    except:
        raise AuthError("Invalid token or token expired", "UNAUTH")
    if decoded:
        return decoded["username"]
    else:
        return None

def get_token():
    token=request.headers.get("Authorization")
    if not(token):
        raise AuthError("Authorization header not present.", "UNAUTH")
    parts=token.split(" ")
    if len(parts)==2:
        my_jwt=parts[1]
    elif len(parts)==1:
        my_jwt=parts[0]
    else:
        raise AuthError("Token format not valid", "UNAUTH")
    try:
        decoded=jwt.decode(my_jwt,"QS App", algorithms=["HS256"])
    except:
        raise AuthError("Invalid token or token expired", "UNAUTH")
    if decoded:
        return token
    else:
        return None