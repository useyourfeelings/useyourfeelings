from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask.ext.login import UserMixin
from . import db, login_manager

from datetime import datetime

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Table, Boolean, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


'''
Role-User  1-n

'''

class Role(db.Model):   #(Role - User) one to many
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer(), unique=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    
    users = db.relationship('User', backref='role', lazy='dynamic')
    
    @staticmethod
    def create_roles():
        roles = {
            (1, 'User', True),
            (100, 'God', False)
        }
        for r in roles:
            role = Role()
            role.level = r[0]
            role.name = r[1]
            role.default = r[2]
            db.session.add(role)
            print('create_roles %r' % role)
        db.session.commit()

    def __repr__(self):
        return '<Role level:%d name:%s default:%d>' % (self.level, self.name, self.default)

class User(UserMixin, db.Model): #(User - Role) many to one  (User - Device) many to many
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    
    telephone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    
    @staticmethod
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
        
    def get_id(self):
        return self.id
        
    def get_name(self):
        return self.username
        
    def is_god(self):
        print('is God %d' % (self.role.name == "God"))
        return self.role.name == "God"

    '''def getRoleId(self)
        return self.role_id
    '''
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))