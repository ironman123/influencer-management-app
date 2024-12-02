from flask import Flask
from flask_cors import CORS
from models import *
from auth import auth 
from utils import celery_init_app

app = Flask(__name__)
CORS(app)

secret_key = "yolo"

app.config["SECRET_KEY"] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_mapping(
    CELERY=dict(  
        broker_url="redis://localhost",
        result_backend="redis://localhost",
        task_ignore_result=True,
        broker_connection_retry_on_startup=True
    ),
)

db.init_app(app)
celery=celery_init_app(app)

with app.app_context():
    db.create_all()
    create_admin()

app.register_blueprint(auth, url_prefix='/auth')



if __name__ == '__main__':
    app.run(debug=True)