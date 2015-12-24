from flask.views import MethodView
from flask import request, redirect, url_for, render_template, jsonify
import arrow
from twilio import twiml
from twilio.util import RequestValidator
import os

class ResourceIndex(MethodView):
    def get(self):
        from schedules import db
        from models.record import Record
        
        all_records = db.session.query(Record).all()
        
        return render_template('index.html', records=all_records)

class ResourceCall(MethodView):
    def get_scheduled_time(self, sent_time, delay_min):
        
        scheduled_time = sent_time.replace(minutes=+delay_min)
        scheduled_time = scheduled_time.datetime
        
        return scheduled_time

    def get_sent_date(self, sent_time):
        return sent_time.format('YYYY-MM-DD')

    def get_sent_timestamp(self, sent_time):
        return sent_time.format('HH:mm:ss')

    def post(self):
        from tasks import schedule_call
        
        phone_number = request.form.get('phoneNumber', None)
        sent_time = arrow.utcnow()
        delay_min = int(request.form.get('delay', None))
        scheduled_time = self.get_scheduled_time(sent_time, delay_min)
        sent_date = self.get_sent_date(sent_time) 
        sent_timestamp = self.get_sent_timestamp(sent_time)    
        schedule_call.apply_async(args=[phone_number, sent_date, sent_timestamp, delay_min], eta=scheduled_time)
       
        return jsonify({'message': 'Call incoming!'})

class ResourceOutboundCall(MethodView):
    def post(self):
        
        if validate_signature():
            phone_number = request.values['Called']
            sent_date = request.args['sent_date']
            sent_timestamp = request.args['sent_timestamp']
            delay_min = request.args['delay_min']
    
            resp = twiml.Response()
            resp.say("Hello! Welcome to the telephone fizz buzz game!")
            
            with resp.gather(timeout=10, finishOnKey="*", action="https://schedule-fizzbuzz.herokuapp.com/handlekey?phone_number="+str(phone_number)+"&sent_date="+str(sent_date)+"&sent_timestamp="+str(sent_timestamp)+"&delay_min="+str(delay_min), method="POST") as g:
                g.say("Please enter your number and then press star.")
            
            return str(resp)
        
        else:
            return 

class ResourceHandleKey(MethodView):
    def get_fizz_buzz(self, resp, digits):
        # generate a range of numbers leading up to the digits entered
        my_digits = (x for x in range(1, int(digits)+1))
        
        for i in my_digits:
            if i % 3 == 0:
                if i % 5 == 0:
                    resp.say("Fizz Buzz")
                else:
                    resp.say("Fizz")
            elif i % 5 == 0:
                resp.say("Buzz")
            else:
                resp.say(str(i))
        
        return resp

    def post(self):
        from schedules import db
        from models.record import Record
        from datetime import datetime

        digits_pressed = request.values.get('Digits', None)
        caller_id = request.values.get('CallSid', None)
        phone_number = request.values.get('Called', None)
        sent_date = request.args['sent_date']
        sent_timestamp = request.args['sent_timestamp']
        sent_time = sent_date + " " + sent_timestamp
        sent_time = datetime.strptime(sent_time, "%Y-%m-%d %H:%M:%S")
        delay_min = request.args['delay_min']
        
        new_record = Record(caller_id, phone_number, sent_time, int(delay_min), int(digits_pressed), None)
        db.session.add(new_record)
        db.session.commit()
        
        resp = twiml.Response()
        resp.say("You've pressed" + digits_pressed)
        resp.say("Now, let's start our fizz buzz game!")
        
        resp = self.get_fizz_buzz(resp, digits_pressed)
        resp.say("That's it! Thanks for playing! Good bye!")
        
        return str(resp)

class ResourceRecording(MethodView):
    def post(self):
        from schedules import db
        from models.record import Record
        
        caller_id = request.values['CallSid']
        link = request.values['RecordingUrl']
        record = Record.query.filter_by(caller_id=caller_id).first()
        record.record_link = link
        db.session.commit()
        
        return

        
def validate_signature():
    validator = RequestValidator(os.environ.get("TWILIO_AUTH_TOKEN"))
    
    if 'X-Twilio-Signature' not in request.headers:
        abort(401)
    else:
        my_url = request.url
        if my_url.startswith('http://'):
            my_url = my_url.replace("http", "https")
        
        params = request.form
        twilio_signature = request.headers['X-Twilio-Signature']
        
        if not validator.validate(my_url, params, twilio_signature):
            abort(401)

    return True

