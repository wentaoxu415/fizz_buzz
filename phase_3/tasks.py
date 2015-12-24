from flask import url_for
from flask import jsonify
from schedules import celery, app
from twilio.rest import TwilioRestClient
from twilio import twiml

twilio_account_sid = app.flask_app.config['TWILIO_ACCOUNT_SID']
twilio_auth_token = app.flask_app.config['TWILIO_AUTH_TOKEN']
twilio_number = app.flask_app.config['TWILIO_NUMBER']

client = TwilioRestClient(account=twilio_account_sid, token=twilio_auth_token)

@celery.task()
def schedule_call(phone_number):
	client.calls.create(from_=twilio_number, to=phone_number, url="https://schedule-fizzbuzz.herokuapp.com/outbound")
		
