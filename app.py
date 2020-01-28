from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Init plugins
db = SQLAlchemy()
loginmanager = LoginManager()
loginmanager.login_view = 'login'

# Init Flask Application
app = Flask(__name__)
app.config.from_object(Config)

# Plugin init app
db.init_app(app)
loginmanager.init_app(app)

# Import routes
from routes import *

# add Commands to the app
from command import add_commands
add_commands(app, db)