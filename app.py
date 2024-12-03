from flask import Flask
from flask_cors import CORS
from models import *
from auth import auth 
from utils import celery_init_app
from worker import daily_reminder,monthly_report

app = Flask(__name__)
CORS(app)

secret_key = "yolo"

app.config["SECRET_KEY"] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_mapping(
    CELERY=dict(  
        broker_url="redis://localhost:6379/0",
        result_backend="redis://localhost:6379/0",
        broker_connection_retry_on_startup=True
    ),
)

db.init_app(app)


with app.app_context():
    db.create_all()
    create_admin()


app.register_blueprint(auth, url_prefix='/auth')

celery=celery_init_app(app)

# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(1,sub.s(1,2),name="Something")

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kkwargs):
    sender.add_periodic_task(15,daily_reminder.s(),name='daily-reminder')
    sender.add_periodic_task(5,monthly_report.s(),name='monthly-report')

if __name__ == '__main__':
    app.run(debug=True)