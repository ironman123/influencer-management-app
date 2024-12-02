from celery import Celery,shared_task
import smtplib
from email.mime.text import MIMEText
import time
import os
from celery.schedules import crontab

from models import db,User

@shared_task
def hello():
    print("Hello Function")
    time.sleep(10)
    print("Hi")
    return "Hello"

@shared_task
def daily_reminder():
    smtpObj = smtplib.SMTP('localhost',1025)

@shared_task
def add(x,y):
    return x+y