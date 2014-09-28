from flask import Flask
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import config
from flask.ext.babel import Babel

from .flasksui import *

flasksui = SUI()

mail = Mail()
db = SQLAlchemy(session_options = {'autocommit':False})

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    flasksui.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    babel = Babel(app, 'en')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
