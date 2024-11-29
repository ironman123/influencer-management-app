from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc,func,or_,and_
from sqlalchemy.types import DateTime
from datetime import datetime
from werkzeug.security import generate_password_hash


db = SQLAlchemy()

#Users Table
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # admin, sponsor, influencer
    flag = db.Column(db.String(20),nullable=False) #initially unauthorized for sponsor and authorized for influencer, then can be set to flagged/authorized

# Sponsor-Specific Table
class Sponsor(db.Model):
    __tablename__ = 'sponsors'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    industry = db.Column(db.String(120), nullable=False)
    user = db.relationship('User', backref=db.backref('sponsor',cascade="all, delete"), uselist=False)

# Influencer-Specific Table
class Influencer(db.Model):
    __tablename__ = 'influencers'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    user = db.relationship('User', backref=db.backref('influencer',cascade="all, delete"), uselist=False)

# Many-to-Many Relationship for Platforms
influencer_platforms = db.Table(
    'influencer_platforms',
    db.Column('influencer_id', db.Integer, db.ForeignKey('influencers.id'), primary_key=True),
    db.Column('platform_id', db.Integer, db.ForeignKey('platforms.id'), primary_key=True)
)

# Platforms Table
class Platform(db.Model):
    __tablename__ = 'platforms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    influencers = db.relationship('Influencer', secondary=influencer_platforms, backref='platforms')

# Campaign Table
class Campaign(db.Model):
    __tablename__ = 'campaigns'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(DateTime(timezone=True), nullable=False)
    end_date = db.Column(DateTime(timezone=True), nullable=False)
    budget = db.Column(db.Float, nullable=False)
    visibility = db.Column(db.String(20), nullable=False)  # public or private
    goals = db.Column(db.Integer, nullable=False)
    flagged = db.Column(db.Boolean, nullable=False, default=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsors.id'), nullable=False)  # Foreign Key to Sponsor
    sponsor = db.relationship('Sponsor', backref=db.backref('campaigns',cascade="all, delete"))

# AdRequest Table
class AdRequest(db.Model):
    __tablename__ = 'ad_requests'
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    to_ = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    from_ = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    payment_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Pending")  # Pending, Accepted, Rejected, Completed
    flagged = db.Column(db.Boolean, nullable=False, default=False)
    campaign = db.relationship('Campaign', backref=db.backref('ad_requests',cascade="all, delete"))
    #influencer = db.relationship('User', backref=db.backref('ad_requests',cascade="all, delete"))  # Influencer is a User
    sender = db.relationship("User", primaryjoin="User.id==AdRequest.from_")
    reciever= db.relationship("User", primaryjoin="User.id==AdRequest.to_")

# Messages Table (Optional)
class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id=db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False)
    ad_request_id = db.Column(db.Integer, db.ForeignKey('ad_requests.id'), nullable=False)
    message_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(DateTime(timezone=True), default=datetime.now)
    ad_request = db.relationship('AdRequest', backref=db.backref('messages',cascade="all, delete"))
    sender = db.relationship('User', backref=db.backref('sent_messages',cascade="all, delete", lazy=True), foreign_keys=[sender_id])

# Function to create admin user
def create_admin():
    admin_email = "user@admin.com"
    existing_admin = User.query.filter_by(email=admin_email).first()
    if not existing_admin:
        admin = User(
            email=admin_email,
            full_name="Admin User",
            password=generate_password_hash("admin"),
            user_type="admin",
            flag='Authorized'
        )
        db.session.add(admin)
    for platform in ['instagram','facebook','youtube']:
        existing_platform = Platform.query.filter_by(name=platform).first()
        if not existing_platform:
            p = Platform(
                name = platform
            )
            db.session.add(p)
    db.session.commit()

# Initialize Database and Admin User
# @app.before_first_request
# def setup():
#     db.create_all()
#     create_admin()

