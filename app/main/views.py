from flask import render_template, request
from flask.ext.login import login_required

from .. import db
from ..models import Role, User
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, InvalidRequestError
from . import main

from sqlalchemy import *#create_engine

import json, datetime

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

#main flask
from flask import Flask, request, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack

#login module
from flask_login import (LoginManager, UserMixin, login_required, login_user,
                             logout_user, make_secure_token, current_user)

@main.route('/')
#@login_required
def dash():
    print("xcc /")
    return redirect(url_for('main.index'))

@main.route('/index')
#@login_required
def index():
    print("xcc /index")
    return render_template("index.html")