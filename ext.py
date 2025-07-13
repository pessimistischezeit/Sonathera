from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = (
    'e3f2d1a4b6c7e8901234567890abcdef1234567890abcdef1234567890abcdef'
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///soundpharmacy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
bcrypt = Bcrypt()

db.init_app(app)
bcrypt.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'