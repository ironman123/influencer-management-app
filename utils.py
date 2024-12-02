from functools import wraps
from flask import request, jsonify
import jwt
from datetime import datetime, timedelta,timezone
from flask import Flask
from celery import Celery,Task

secret_key = "yolo"


def celery_init_app(app:Flask)->Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs:object)->object:
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery_app = Celery(app.name,task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"]=celery_app
    return celery_app

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
        return f(data,*args,**kwargs)
    return wrapper

def tokenizer(email):
    token = jwt.encode(
               {'email':email,'exp':datetime.now(timezone.utc) + timedelta(hours=24)},
               secret_key,
               algorithm = "HS256"
           )
    return token