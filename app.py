from flask import Flask
from flask_cors import CORS
from models import *
from auth import auth 

app = Flask(__name__)
CORS(app)

secret_key = "yolo"

app.config["SECRET_KEY"] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    create_admin()

app.register_blueprint(auth, url_prefix='/auth')



if __name__ == '__main__':
    app.run(debug=True)