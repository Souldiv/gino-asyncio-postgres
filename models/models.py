import asyncio
from datetime import datetime
import enum
from create_db import db


class MyEnum(enum.Enum):
	product = "PRODUCT"
	checkout = "CHECKOUT"

class Accounts(db.Model):
	__tablename__ = 'Accounts'

	id = db.Column(db.Integer(), primary_key=True)
	created_at = db.Column(db.DateTime(), default=datetime.utcnow)
	updated_at = db.Column(db.DateTime(), onupdate=datetime.utcnow, default=datetime.utcnow)
	name = db.Column(db.Unicode())
	account_key = db.Column(db.Unicode())
	ab_test_on = db.Column(db.Boolean())

class Sessions(db.Model):
	__tablename__ = 'Sessions'
	id = db.Column(db.Integer(), primary_key=True)
	created_at = db.Column(db.DateTime(), default=datetime.utcnow)
	updated_at = db.Column(db.DateTime(), onupdate=datetime.utcnow, default=datetime.utcnow)
	account_id = db.Column(db.Integer(), db.ForeignKey('Accounts.id'))
	session_key = db.Column(db.String())
	client_ip = db.Column(db.String())

class Interactions(db.Model):
	__tablename__ = 'Interactions'
	id = db.Column(db.Integer(), primary_key=True)
	created_at = db.Column(db.DateTime(), default=datetime.utcnow)
	updated_at = db.Column(db.DateTime(), onupdate=datetime.utcnow, default=datetime.utcnow)
	account_id = db.Column(db.Integer(), db.ForeignKey('Accounts.id'))
	session_key = db.Column(db.String())
	client_ip = db.Column(db.String())
	client_url = db.Column(db.String())
	interaction_type = db.Column(db.Enum(MyEnum), nullable=True)
	ab_test = db.Column(db.Boolean(), default=False)
	object_shown = db.Column(db.Boolean(), nullable=True)