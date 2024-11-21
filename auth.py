from flask import Blueprint, request
from flask import jsonify
from models import *
from utils import token_required,tokenizer
from werkzeug.security import check_password_hash


auth = Blueprint('auth', __name__)


@auth.route('/signin', methods=['POST'])
def login():
    if request.method == 'POST':
       data = request.json
       email = data['email']
       password = data['password']
       user = User.query.filter_by(email = email).first()

       if user and check_password_hash(user.password,password):
          user_type = user.user_type
          token = tokenizer(email)
          return jsonify({'message':'SignIn Successful!','token':token,'user_type':user_type}),200
       return jsonify({'message':'Invalid Credentials'}),401



@auth.route('/temp', methods=['POST'])
@token_required
def temp():
   if request.method == 'POST':
      print("Route entered")
      return "yolo"



# @auth.route('/signout')
# def logout():
#     return "Logged out"