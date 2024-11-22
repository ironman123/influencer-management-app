from flask import Blueprint, request, jsonify
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
         return jsonify({'message':'SignIn Successful!','token':token,'email':email,'user_type':user_type}),200
      return jsonify({'message':'Invalid Credentials'}),401

@auth.route('/register', methods=['POST'])
def register():
   if request.method=='POST':
     data = request.json
   
   # Extract the common fields
   email = data.get('email')
   full_name = data.get('fullname')
   password = data.get('password')
   user_type = data.get('userType')
   
   # Validate required fields
   if not all([email, full_name, password, user_type]):
      return jsonify({'message': 'All fields are required'}), 400
   
   # Check if user already exists
   user = User.query.filter_by(email=email).first()
   if user:
      return jsonify({'message': 'User already exists'}), 400
   
   # Hash the password
   hashed_password = generate_password_hash(password)
   
   # Create the User entry
   new_user = User(
      email=email,
      full_name=full_name,
      password=hashed_password,
      user_type=user_type
   )
   db.session.add(new_user)
   db.session.commit()
   
   # Handle specific user types
   if user_type == "sponsor":
      industry = data.get('industry')
      if not industry:
         return jsonify({'message': 'Industry is required for sponsor'}), 400
      sponsor = Sponsor(
         id=new_user.id,  # Use the ID of the created User
         industry=industry
      )
      db.session.add(sponsor)
   elif user_type == "influencer":
      platforms = data.get('platforms', [])
      influencer = Influencer(
         id=new_user.id  # Use the ID of the created User
      )
      db.session.add(influencer)
      # Add influencer's platforms if provided
      for platform in platforms:
         platform = Platform.query.filter_by(name =platform).first()
         if platform:
            influencer.platforms.append(platform)
   else:
      return jsonify({'message': 'Invalid user type'}), 400
   # Commit all changes
   db.session.commit()
   # u = User.query.filter_by(email='rajul@email.com').first()
   # if u:
   #    db.session.delete(u)
   #    db.session.commit()
   return jsonify({'message': 'User registered successfully'}), 201
     
     

@auth.route('/check-token', methods=['GET'])
@token_required
def check_token(decoded_data):
    print(decoded_data)
    return jsonify({'message': 'Token is valid!', 'data': decoded_data}), 200



@auth.route('/temp', methods=['POST'])
@token_required
def temp():
   if request.method == 'POST':
      print("Route entered")
      return "YOLO"



# @auth.route('/signout')
# def logout():
#     return "Logged out"