from flask import Blueprint, request, jsonify
from models import *
from utils import token_required,tokenizer
from werkzeug.security import check_password_hash
from datetime import timedelta,timezone
from sqlalchemy import or_
from celery.result import AsyncResult


auth = Blueprint('auth', __name__)


@auth.route('/results/<string:id>')
def get_results(id):
   result = AsyncResult(id)
   return [result.status,result.result]

@auth.route('/signin', methods=['POST'])
def login():
   if request.method == 'POST':
      data = request.json
      email = data['email']
      password = data['password']
      user = User.query.filter_by(email = email).first()

      if user and check_password_hash(user.password,password):
         if user.flag == 'Unauthorized':
            return jsonify({'message':'Unauthorized Access!'}),403
         token = tokenizer(email)
         userType = user.user_type
         userName=user.full_name
         userID = user.id
         return jsonify({'message':'SignIn Successful!','token':token,'userID':userID,'userName':userName,'email':email,'userType':userType}),200
      else:
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
      user_type=user_type,
      flag='Authorized' if user_type == 'Influencer' else 'Unauthorized'
   )
   db.session.add(new_user)
   db.session.commit()
   
   # Handle specific user types
   if user_type == "Sponsor":
      industry = data.get('industry')
      if not industry:
         return jsonify({'message': 'Industry is required for sponsor'}), 400
      sponsor = Sponsor(
         id=new_user.id,  # Use the ID of the created User
         industry=industry
      )
      db.session.add(sponsor)
   elif user_type == "Influencer":
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

@auth.route('/campaigns',methods=['GET','POST','PUT'])
@token_required
def campaigns(data):
   if request.method == "GET":
      #data = request.json
      #search_query = request.headers.get('search-query','').lower()

      # if search_query:
      #    print("Search Query: ",search_query)

      #print("Data: ",data)
      
      email = data.get("email")
      owner = request.args.get('owner')
      if not email:
         return jsonify({"message": "Unauthorized access"}), 403
      user = User.query.filter_by(email=email).first()
       
      # Query for all public campaigns or private campaigns owned by the user or all if user is admin
      if user.user_type == "Influencer":
         campaigns = (Campaign.query.join(Sponsor).join(User)).filter(
            or_(Campaign.visibility == "public",
               and_(Campaign.visibility == "private",User.email == email)
               )
            ).all()
      elif user.user_type == "Sponsor":
         print("The owner is:",owner,type(owner))
         if owner:
            campaigns = (Campaign.query.join(Sponsor).join(User)).filter(
               and_(
                  User.email == email,
                  Campaign.sponsor_id==owner,
                  Campaign.flagged==0,
                  Campaign.end_date > datetime.now(timezone.utc))
            ).all()
         else:
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

      name=data.get('name')
      description=data.get('description')
      visibility=data.get('visibility')
      start_date=datetime.fromisoformat(data.get('startDate'))
      end_date=datetime.fromisoformat(data.get('endDate'))
      budget=float(data.get('budget'))
      goals=int(data.get('goals'))

      # Validate required fields
      #print([name, description, start_date, end_date,budget,visibility,goals])
      #if not all([name, description, start_date, end_date,budget,visibility,goals]):
      #   return jsonify({'message': 'All fields are required'}), 400
   
      sponsor = Sponsor.query.join(User).filter_by(email=email).first()
      if not sponsor:
         return jsonify({'message': 'Sponsor not found'}), 404
      elif sponsor.user.flag == 'Flagged':
         return jsonify({'message': 'Flagged User Action Not Allowed!'}), 403

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
      
   if request.method=='PUT':
      email=data['email']
      if not email:
         return jsonify({"message": "Unauthorized access"}), 403
      user = User.query.filter_by(email=email).first()
      if not user:
         return jsonify({"message": "User Not found!"}), 404
      data=request.json

      id=data['id']
      campaign = Campaign.query.filter_by(id=id).first()
      if not campaign:
            return jsonify({'message': 'Campaign not found'}), 404

      if user.user_type != 'admin':
         name=data.get('name')
         description=data.get('description')
         visibility=data.get('visibility')
         start_date=datetime.fromisoformat(data.get('startDate'))
         end_date=datetime.fromisoformat(data.get('endDate'))
         budget=float(data.get('budget'))
         goals=int(data.get('goals'))

         sponsor = Sponsor.query.join(User).filter_by(email=email).first()
         if not sponsor:
            return jsonify({'message': 'Sponsor not found'}), 404
         elif sponsor.user.flag == 'Flagged':
            return jsonify({'message': 'Flagged User, Action Not Allowed!'}), 403

         campaign.name=name
         campaign.description=description
         campaign.visibility=visibility
         campaign.start_date=start_date
         campaign.end_date=end_date
         campaign.budget=budget
         campaign.goals=goals
         db.session.commit()
         return jsonify({'message': 'Campaign Edited successfully', 'campaign_id': campaign.id}), 201
      else:
         flag = data['flag']
         print(flag,":")
         if not flag:
            return jsonify({'message': 'Flag value is required'}), 400
         if flag == 'Active':
            campaign.flagged=True
            flag = 'Flagged'
         elif flag == 'Flagged':
            campaign.flagged=False
            flag = 'Active'
         elif flag == 'Completed':
            return jsonify({'message': 'Completed Campaign Cannot Be Flagged!!!', 'flag': flag}),201   
         db.session.commit()
         return jsonify({'message': 'Flag updated successfully', 'flag': flag}),201

@auth.route('/users',methods=['GET','PUT'])
@token_required
def users(data):
   email =data.get('email')
   if not email:
      return jsonify({"meassage": "Unauthorized access"}), 403
   user = User.query.filter_by(email=email).first()
   
   # if user.user_type != 'admin':
   #    return jsonify({"message": "Unauthorized access"}), 403
   
   if request.method == 'GET':
      user_type = request.args.get('type')

      query = User.query

      if user_type:
            query = query.filter_by(user_type=user_type)

      users = query.all()
      users_data=[]
      
      for user in users:
        requests = AdRequest.query.filter_by(influencer_id=user.id,status='Completed').all()
        
        if requests:
            avg_rating = sum(request.rating for request in requests) / len(requests)
        else:
            avg_rating = None  
        
        users_data.append({
            'id': user.id,
            'name': user.full_name,
            'userType': user.user_type,
            'flag': user.flag,
            'email': user.email,
            'rating': avg_rating  # Include the calculated average rating
        })

      
         
      return jsonify(users_data),201
   
   elif request.method =='PUT':
      data = request.json
      id = data['id']
      flag=data['flag']
      user = User.query.filter_by(id=id).first()

      if not user:
         return jsonify({'message': 'User not found'}), 404
      if not flag:
         return jsonify({'message': 'Flag value is required'}), 400
      
      user.flag = flag
      db.session.commit()
      return jsonify({'message': 'Flag updated successfully', 'flag': user.flag}),201


@auth.route('/requests',methods=['GET','PUT','POST'])
@token_required
def requests(data):
   email = data['email']
   if not email:
      return jsonify({"message": "Unauthorized access!!"}), 403
   user = User.query.filter_by(email=email).first()
   if not user:
        return jsonify({"message": "User not found!"}), 404
   elif user.flag == 'Flagged':
         return jsonify({'message': 'Flagged User, Action Not Allowed!'}), 403
   
   user_type = user.user_type
   
   if request.method == "GET":
      if user_type == "Sponsor":
         requests = AdRequest.query \
         .join(Campaign) \
         .filter_by(sponsor_id = user.id) \
         .all()
         
      elif user_type == "Influencer":
         requests = AdRequest.query \
         .filter_by(influencer_id = user.id) \
         .all()
      elif user_type == "admin":
         requests = AdRequest.query.all()
      else:
         return jsonify({"message": "User type not recognized!"}), 400
      
      request_data = [
         {
            'id':req.id,
            'campaignName':req.campaign.name,
            'sponsor':req.campaign.sponsor.user.full_name,
            'influencer':req.influencer.full_name,
            'campaign_id':req.campaign.id,
            'sponsor_id':req.campaign.sponsor_id,
            'influencer_id':req.influencer_id,
            'requirements':req.requirements,
            'paymentAmount':req.payment_amount,
            'status':req.status,
            'rating':req.rating,
            'to_':req.to_,
            'from_':req.from_,
            'toUser':req.reciever.full_name,
            'fromUser':req.sender.full_name,
            'start_date':req.campaign.start_date,
            'end_date':req.campaign.end_date
         }
         for req in requests
      ]
      return jsonify(request_data),201
      
   
   elif request.method== "POST":
      data = request.json
      print(data)
      to_=data['to_']
      from_=data['from_']
      campaign_id=data['campaign_id']
      influencer_id=data['influencer_id']
      requirements=data['requirements']
      payment_amount=data['payment_amount']
      status=data['status']
      
      if int(from_) != user.id:
         return jsonify({'message': 'Campaign Does not belong to Sponsor'}), 403

      campaign = Campaign.query.filter_by(id=campaign_id).first()
      if not campaign:
         return jsonify({'message': 'Campaign not found'}), 404
      elif campaign.flagged:
         return jsonify({'message': 'Flagged Campaign, Action Not Allowed!'}), 403
   
      new_request = AdRequest(
         to_=to_,
         from_=from_,
         campaign_id=campaign_id,
         influencer_id=influencer_id,
         requirements=requirements,
         payment_amount=payment_amount,
         status=status
      )
      try:  
         db.session.add(new_request)
         db.session.commit()
         return jsonify({'message': 'Request created successfully', 'request_id': new_request.id}), 201
      except Exception as e:
         db.session.rollback()
         return jsonify({'message': 'Failed to create Ad Request', 'error': str(e)}), 500
      
   elif request.method=='PUT':
      email=data['email']
      if not email:
         return jsonify({"message": "Unauthorized access"}), 403
      user = User.query.filter_by(email=email).first()
      if not user:
         return jsonify({"message": "User Not found!"}), 404
      data=request.json
      request_id = data['id']
      req = AdRequest.query.filter_by(id=request_id).first()
      if not req:
         return jsonify({'message': 'Ad Request not found'}), 404
      
      status = data['status']
      if user.user_type == 'Sponsor':
         # if not status:
         #    return jsonify({'message': 'Status value is required'}), 400
         print(data)
         if status and req.status == 'Accepted' and status == 'Completed':
            rating = data['rating']
            if rating not in [0,1,2,3,4,5]:
               return jsonify({'message': 'Rating not found or Invalid Rating!'}), 404
            if user.user_type != 'Sponsor':
               return jsonify({'message': 'Action Not allowed to a Non Sponsor!'}), 304
            req.status = status
            req.rating = rating
            try:
               db.session.commit()
               return jsonify({'message': 'Request updated successfully','status':status}), 200
            except Exception as e:
               db.session.rollback()
               return jsonify({'message': 'Failed to update request', 'error': str(e)}), 500
         elif status and req.status == 'Pending' and status in ['Accepted', 'Rejected']:
            if req.from_ == user.id:
               return jsonify({'message': 'Owner cannot Accept or Reject own Request'}), 304
            req.status = status
            try:
               db.session.commit()
               return jsonify({'message': 'Request updated successfully','status':status}), 200
            except Exception as e:
               db.session.rollback()
               return jsonify({'message': 'Failed to update request', 'error': str(e)}), 500
         
         req.requirements = data['requirements']
         req.payment_amount = data['payment_amount']
         try:
            db.session.commit()
            return jsonify({'message': 'Request updated successfully'}), 200
         except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Failed to update request', 'error': str(e)}), 500
         
      elif user.user_type == 'Influencer':
         if status and req.status == 'Pending' and status in ['Accepted', 'Rejected']:
            req.status = status
            if req.from_ == user.id:
               return jsonify({'message': 'Owner cannot Accept or Reject own Request'}), 304
            try:
               db.session.commit()
               return jsonify({'message': 'Request updated successfully','status':status}), 200
            except Exception as e:
               db.session.rollback()
               return jsonify({'message': 'Failed to update request', 'error': str(e)}), 500
         else:
            return jsonify({'message': 'Invalid status transition for Influencer'}), 400

      
@auth.route('/messages',methods=['GET','POST'])
@token_required
def messages(data):
   
   email= data['email']
   if not email:
      return jsonify({"message": "Unauthorized access"}), 403
   
   user = User.query.filter_by(email=email).first()
   if not user:
        return jsonify({"message": "User not found!"}), 404

   if request.method == 'GET':
      ad_request_id = request.args.get('ad_request_id')
      if not ad_request_id:
         return jsonify({"message": "Missing Ad Request ID"}), 404
        # Fetch all messages for the specific ad_request_id
      messages = Message.query.filter_by(ad_request_id=ad_request_id).all()
        
        # If no messages are found
      if not messages:
         return jsonify({"message": "No messages found for this Ad Request ID"}), 404
      
      result = []
      for message in messages:
         result.append({
            'id': message.id,
            'sender_name': message.sender.full_name,  # Assuming 'sender' is a relationship in the Message model
            'message_text': message.message_text,
            'timestamp': message.timestamp.isoformat(),  # Return timestamp in ISO format
         })

      return jsonify(result), 200
   
   elif request.method == 'POST':
        # Handle the POST request for creating a new message
      message_text = request.json.get('message_text')
      ad_request_id = request.json.get('ad_request_id')
        
      if not message_text:
         return jsonify({"message": "Message text is required"}), 400
        
        # Create a new message object and associate it with the user
      new_message = Message(
         ad_request_id=ad_request_id,
         message_text=message_text,
         sender_id=user.id  # sender_id is the user's ID
      )
        
      try:
         # Add and commit the new message to the database
         db.session.add(new_message)
         db.session.commit()

         return jsonify({"message": "Message sent successfully!"}), 201
      
      except Exception as e:
         db.session.rollback()
         return jsonify({"message": f"An error occurred while sending the message: {str(e)}"}), 500

   
   # if request.method == 'GET':
   #    messages = Message.query.filter_by(ad_request_id=ad_request_id).all()

   #    if not messages:
   #          return jsonify({"message": "No messages found for this Ad Request ID"}), 404
      
   return

   


@auth.route('/temp', methods=['GET'])
#@token_required
def temp():
   if request.method == 'GET':
      #pass
       campaign1 = Campaign(
          name="Burger Burger",
          description="Promoting winter-themed products.",
          start_date=datetime.now(timezone.utc),
          end_date=datetime.now(timezone.utc) + timedelta(days=30),
          budget=5000.0,
          visibility="public",
          goals=5,
          flagged=True,
          sponsor_id=3
       )
       campaign2 = Campaign(
          name="Pizza Pizza",
          description="Massive discounts for summer products.",
          start_date=datetime.now(timezone.utc) - timedelta(days=60),
          end_date=datetime.now(timezone.utc) - timedelta(days=30),
          budget=8000.0,
          visibility="private",
          goals=10,
          sponsor_id=3
       )
       db.session.add(campaign1)
       db.session.add(campaign2)
       db.session.commit()
      
   return jsonify({'message': 'Entries Added successfully'}), 201 



# @auth.route('/signout')
# def logout():
#     return "Logged out"