from functools import wraps
from flask import request, jsonify
import jwt
from datetime import datetime, timedelta,timezone

secret_key = "yolo"



def token_required(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message':'Token Missing'}), 401
        try:
            data = jwt.decode(token,secret_key,algorithms=["HS256"]) #options={"verify_exp": True} default
            # exp_time = datetime.fromtimestamp( data.get("exp"),timezone.utc)
            # curr_time = datetime.now(timezone.utc)
            # print(exp_time)
            # print(curr_time)
            # if(exp_time < curr_time ):
            #     raise jwt.ExpiredSignatureError()
        except jwt.ExpiredSignatureError:
            print("Token Expired!")
            return jsonify({'message':'Token Expired!'}),401
        except jwt.InvalidTokenError:
            print("Token Invalid!")
            return jsonify({'message':'Invalid Token!'}),401
        return f(*args,**kwargs)
    return wrapper

def tokenizer(email):
    token = jwt.encode(
               {'email':email,'exp':datetime.now(timezone.utc) + timedelta(seconds=10)},
               secret_key,
               algorithm = "HS256"
           )
    return token