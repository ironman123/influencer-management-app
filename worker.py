from celery import Celery,shared_task
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import os
import datetime
from datetime import timedelta,timezone,datetime,date
from celery.schedules import crontab
from models import db,User,AdRequest,Campaign
from sqlalchemy import or_
from jinja2 import Template
from smtplib import SMTP

@shared_task
def daily_reminder():
    print('DAILY REMINDER WORKING')
    today = datetime.now(timezone.utc).date()
    ten_days_later = today + timedelta(days=10)

    # Query the AdRequest table with the filters
    ad_requests = (
        db.session.query(AdRequest)
        .join(Campaign)  # Join Campaign to filter by its end_date
        .filter(Campaign.end_date >= today)  # Campaign end_date is exactly 10 days from today
        .filter(or_(AdRequest.status == "Accepted",AdRequest.status == "Pending"))  # AdRequest status is 'Accepted'
        .all()
    )
    smtpObj = SMTP('localhost',1025)
    for request in ad_requests:
        print(request.status)
        if request.status == "Pending":
            if(request.from_ == request.influencer_id):
                smtpObj.sendmail("nekonet@email.com",request.campaign.sponsor.user.email,f"You still have PENDING requests from {request.influencer.full_name} : ({request.influencer.email}).")
            else:
                smtpObj.sendmail("nekonet@email.com",request.influencer.email,f"You still have PENDING requests from {request.campaign.sponsor.user.full_name} : ({request.campaign.name}).")
        elif request.status == "Accepted":
            if(request.from_ == request.influencer_id):
                smtpObj.sendmail("nekonet@email.com",request.campaign.sponsor.user.email,f"You still have INCOMPLETE requests from {request.influencer.full_name} : ({request.influencer.email}).")
            else:
                smtpObj.sendmail("nekonet@email.com",request.influencer.email,f"You still have INCOMPLETE requests from {request.campaign.sponsor.user.full_name} : ({request.campaign.name}).")
            #smtpObj.sendmail("nekonet@email.com",request.influencer.email,f"You still have INCOMPLETE requests for ({request.campaign.sponsor.user.full_name}) : {request.campaign.name}.")

@shared_task
def monthly_report_sponsor():
    print('MONTHLY REPORT WORKING')

    # Fetch all AdRequests joined with Campaign
    requests = db.session.query(AdRequest).join(Campaign).all()

    # Query all sponsors (filter by user_type == 'sponsor')
    sponsors = db.session.query(User).filter(User.user_type == 'Sponsor').all()

    # Open the template for rendering
    with open("templates/influencer-report.html") as file:
        template = Template(file.read())

    # Configure SMTP server
    server = SMTP(host="localhost", port=os.environ.get("SMTP", 1025))

    # Loop over each sponsor and send the email with their specific report
    for sponsor in sponsors:
        # Include all requests, not just the sponsor's related requests
        sponsor_requests = requests
        
        if not sponsor_requests:
            continue  # Skip if there are no requests at all (this is more of a safeguard)

        # Create the email
        mail = MIMEMultipart()
        mail["FROM"] = "nekonet@email.com"
        mail["TO"] = sponsor.email  # Send to the sponsor's email
        mail["SUBJECT"] = "Monthly Report"

        # Render the template with the sponsor's specific requests (all requests in this case)
        html_content = template.render(user=sponsor, requests=sponsor_requests)
        html = MIMEText(html_content, "html")
        mail.attach(html)

        server.sendmail(mail["FROM"], mail["TO"], mail.as_string())

@shared_task
def monthly_report_influencer():
    today = datetime.now(timezone.utc).date()
    first_day_of_month = date(year=today.year, month=today.month, day=1)

    # Query AdRequests and join with User
    ad_requests = (
        db.session.query(User, AdRequest)
        .join(Campaign, AdRequest.campaign_id == Campaign.id)
        .filter(Campaign.end_date > first_day_of_month)
        .all()
    )

    # Group AdRequests by user
    user_reports = {}
    for influencer, ad_request in ad_requests:
        if influencer not in user_reports:
            user_reports[influencer] = []
        user_reports[influencer].append(ad_request)



    with open("templates/influencer-report.html") as file:
        template = Template(file.read())
    server = SMTP(host="localhost", port=os.environ.get("SMTP", 1025))
    
    nonInfluencerIds = [user.id for user in db.session.query(User.id).filter(User.user_type != 'Influencer').all()]

    for influencer, requests in user_reports.items():      
        # Filter requests belonging to the current influencer
        user_requests = [req for req in user_reports[influencer] if req.influencer_id == influencer.id]
        if not requests:
            continue  # Skip if there are no requests for this user
        if influencer.id in nonInfluencerIds:
            continue
        mail = MIMEMultipart()
        mail["FROM"] = "admin@example.com"
        mail["To"] = influencer.email  
        mail["SUBJECT"] = "Your Monthly Report"
        # Render the template with user-specific requests
        html_content = template.render(user=influencer, requests=user_requests)
        html = MIMEText(html_content, "html")
        mail.attach(html)
        # Send email using your configured SMTP server
        server.sendmail(mail["FROM"], mail["To"], mail.as_string())

    server.quit()

@shared_task
def monthly_report():
    today = datetime.now(timezone.utc).date()
    first_day_of_month = date(year=today.year, month=today.month, day=1)

    # Query AdRequests and join with User
    ad_requests = (
        db.session.query(User, AdRequest)
        .join(Campaign, AdRequest.campaign_id == Campaign.id)
        .filter(Campaign.end_date > first_day_of_month)
        .all()
    )

    # Group AdRequests by user
    user_reports = {}
    for user, ad_request in ad_requests:
        if user not in user_reports:
            user_reports[user] = []
        user_reports[user].append(ad_request)

    with open("template/monthly-report.html") as file:
        template = Template(file.read())

    server = SMTP(host="localhost", port=os.environ.get("SMTP", 1025))

    for user, requests in user_reports.items():
        mail = MIMEMultipart()
        mail["FROM"] = "admin@example.com"
        mail["To"] = user.email  # User-specific email
        mail["SUBJECT"] = "Your Monthly Report"

        # Render the template with user-specific requests
        html_content = template.render(user=user, requests=requests)
        html = MIMEText(html_content, "html")
        mail.attach(html)

        # Send email
        server.sendmail("admin@example.com", user.email, mail.as_string())

    server.quit()

@shared_task
def sub(x,y):
    print("Running>.")
    return x-y
