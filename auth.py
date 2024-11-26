from flask import Blueprint, request, jsonify
from models import *
from utils import token_required,tokenizer
from werkzeug.security import check_password_hash
from datetime import timedelta,timezone
from sqlalchemy import or_


auth = Blueprint('auth', __name__)


@auth.route('/signin', methods=['POST'])
def login():
   if request.method == 'POST':
      data = request.json
      email = data['email']
      password = data['password']
      user = User.query.filter_by(email = email).first()

      if user and check_password_hash(user.password,password):
         token = tokenizer(email)
         userType = user.user_type
         userName=user.full_name
         userID = user.id
         return jsonify({'message':'SignIn Successful!','token':token,'userID':userID,'userName':userName,'email':email,'userType':userType}),200
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
         platform = Platform.query.filter_by(name=platform).first()
         if platform:
            influencer.platforms.append(platform)
   else:
      return jsonify({'message': 'Invalid user type'}), 400
   # Commit all changes
   db.session.commit()
   
   return jsonify({'message': 'User registered successfully'}), 201
     
     

@auth.route('/check-token', methods=['GET'])
@token_required
def check_token(decoded_data):
    print(decoded_data)
    return jsonify({'message': 'Token is valid!', 'data': decoded_data}), 200

@auth.route('/campaigns',methods=['GET','POST'])
@token_required
def campaigns(data):
   if request.method == "GET":
      #data = request.json
      #search_query = request.headers.get('search-query','').lower()

      # if search_query:
      #    print("Search Query: ",search_query)

      #print("Data: ",data)
      
      email = data.get("email")
      if not email:
         return jsonify({"error": "Unauthorized access"}), 403
      userType = User.query.filter_by(email=email).first().user_type
       
      # Query for public campaigns or private campaigns owned by the user or all if user is admin
      if userType != "admin":
         campaigns = (Campaign.query.join(Sponsor).join(User)).filter(
            or_(Campaign.visibility == "public",
               and_(Campaign.visibility == "private",User.email == email)
               )
            ).all()
      else:
         campaigns = Campaign.query.all()

      campaigns_data = [
        {
            'id': campaign.id,
            'name': campaign.name,
            'description': campaign.description,
            'start_date': campaign.start_date.strftime('%Y-%m-%d'),
            'end_date': campaign.end_date.strftime('%Y-%m-%d'),
            'budget': campaign.budget,
            'visibility': campaign.visibility,
            'goals': campaign.goals,
            'sponsor_id': campaign.sponsor_id,
            'status': "Flagged" if campaign.flagged else "Active" if campaign.end_date.replace(tzinfo=timezone.utc) > datetime.now(timezone.utc) else "Completed",
            'ownerID': campaign.sponsor.user.email,
            'owner':campaign.sponsor.user.full_name
        }
        
        for campaign in campaigns
      ]
      return jsonify(campaigns_data),201
   
   if request.method == "POST":
      email = data.get("email")
      data = request.json
      print("Form Data for Campaign: ",data)

      name=data.get('name')
      description=data.get('description')
      visibility=data.get('visibility')
      start_date=datetime.fromisoformat(data.get('startDate'))
      end_date=datetime.fromisoformat(data.get('endDate'))
      budget=float(data.get('budget'))
      goals=int(data.get('goals'))

      # Validate required fields
   if not all([name, description, start_date, end_date,budget,visibility,goals]):
      return jsonify({'message': 'All fields are required'}), 400
   
   sponsor = Sponsor.query.join(User).filter_by(email=email).first()
   if not sponsor:
      return jsonify({'message': 'Sponsor not found'}), 404
   
   new_campaign = Campaign(
        name=name,
        description=description,
        start_date=start_date,
        end_date=end_date,
        budget=budget,
        visibility=visibility,
        goals=goals,
        sponsor_id=sponsor.id
    )

    # Add the campaign to the database
   try:
      db.session.add(new_campaign)
      db.session.commit()
      return jsonify({'message': 'Campaign created successfully', 'campaign_id': new_campaign.id}), 201
   except Exception as e:
      db.session.rollback()
      return jsonify({'message': 'Failed to create campaign', 'error': str(e)}), 500



@auth.route('/temp', methods=['GET'])
@token_required
def temp(data):
   if request.method == 'GET':
      campaign1 = Campaign(
          name="Winter Sale",
          description="Promoting winter-themed products.",
          start_date=datetime.now(timezone.utc),
          end_date=datetime.now(timezone.utc) + timedelta(days=30),
          budget=5000.0,
          visibility="public",
          goals=5,
          sponsor_id=2
      )

      campaign2 = Campaign(
          name="Summer Sale",
          description="Massive discounts for summer products.",
          start_date=datetime.now(timezone.utc) - timedelta(days=60),
          end_date=datetime.now(timezone.utc) - timedelta(days=30),
          budget=8000.0,
          visibility="private",
          goals=10,
          flagged=True,
          sponsor_id=2
      )

      db.session.add(campaign1)
      db.session.add(campaign2)
      db.session.commit()
   return jsonify({'message': 'Entries Added successfully'}), 201 



# @auth.route('/signout')
# def logout():
#     return "Logged out"