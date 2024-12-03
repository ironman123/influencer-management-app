from celery import Celery,shared_task
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import os
import datetime
from datetime import timedelta,timezone,datetime
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
def monthly_report():
    print('MONTHLY REPORT WORKING')
    requests = db.session.query(AdRequest).join(Campaign).all()
    with open("templates/influencer-report.html") as file:
        template = Template(file.read())

    server = SMTP(host="localhost",port=os.environ.get("SMTP",1025))
    mail = MIMEMultipart()
    mail["FROM"] = "nekonet@email.com"
    mail["TO"] = "user@admin.com"
    mail["SUBJECT"] = "Monthly Report"

    html = MIMEText(template.render(requests),"html")
    mail.attach(html)
    server.send("nekonet@email.com","user@admin.com",mail.as_string())


@shared_task
def sub(x,y):
    print("Running>.")
    return x-y
