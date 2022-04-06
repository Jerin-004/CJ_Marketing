from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import os


pickFolder = os.path.join('static','images')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = pickFolder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config["SECRET_KEY"] = "8efcae14129733768307aaa5"
db = SQLAlchemy(app)
admin = Admin(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = 'info'
from market import route

