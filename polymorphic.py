import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, ValidationError, fields, pprint, pre_load

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'polymorphic.db')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    driver = db.relationship('Driver', uselist=False, back_populates='user')
    manager = db.relationship('Manager', uselist=False, back_populates='user')

class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driving_license = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='driver')

class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='manager')

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    driver = fields.Nested('DriverSchema', only=['driving_license'])
    manager = fields.Nested('ManagerSchema', only=['designation'])

class ManagerSchema(Schema):
    id = fields.Int(dump_only=True)
    designation = fields.Str()
    user = fields.Nested(UserSchema, only=['name'])

class DriverSchema(Schema):
    id = fields.Int(dump_only=True)
    driving_license = fields.Str()
    #user = fields.Nested(UserSchema())

db.create_all()
db.session.commit()
user_schema = UserSchema()
users_schema = UserSchema(many=True)
manager_schema = ManagerSchema()
managers_schema = ManagerSchema(many=True)

user0 = User(name='User 0')
user1 = User(name='User 1')
db.session.add(user0)
db.session.add(user1)

db.session.commit()
manager = Manager(designation='Some designation', user=user0)
driver = Driver(driving_license='Some driving license', user=user1)

db.session.add(manager)
db.session.add(driver)
db.session.commit()
#users = User.query.all()
managers = Manager.query.all()
#result = users_schema.dump(users)
result = managers_schema.dump(managers)
pprint(result,  indent=2)
"""
manager = User.query.all()
for i in manager:
    print(i.manager.designation)


holi = User.query.all()
for i in holi:
    print(i.driver.driving_license)
"""
