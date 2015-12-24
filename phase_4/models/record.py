from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, String

from schedules import db

Base = declarative_base()

class Record(db.Model):
	__tablename__ = 'results'

	id = db.Column(Integer, primary_key=True)
	caller_id = db.Column(String(200), nullable=True)
	phone_number = db.Column(String(50), nullable=False)
	time = db.Column(DateTime, nullable=False)
	delay = db.Column(Integer, nullable=False)
	fizz_buzz = db.Column(Integer, nullable=False)
	record_link = db.Column(String(200), nullable=True)


	def __init__(self, caller_id, phone_number, time, delay, fizz_buzz, record_link):
		self.caller_id = caller_id
		self.phone_number = phone_number
		self.time = time
		self.delay = delay 
		self.fizz_buzz = fizz_buzz
		self.record_link = record_link

	def __repr__(self):
		return '<Record %r>' % self.phone_number


