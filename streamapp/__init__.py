from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import os
 
#os.environ['FLASK_ENV'] = 'development'
SECRET_KEY = os.urandom(32)

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = SECRET_KEY
# CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test_lastfm.db"
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Bootstrap(app)
db = SQLAlchemy(app)

login_manager = LoginManager(app)

from streamapp import routes