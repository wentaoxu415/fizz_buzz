from flask.views import MethodView
from flask import request, redirect, url_for, render_template, jsonify
import arrow
from twilio import twiml
from twilio.util import RequestValidator
import os

class ResourceIndex(MethodView):
    def get(self):
        return render_template('index.html')

class ResourceCall(MethodView):
    def post(self):
        from tasks import schedule_call
        phone_number = request.form.get('phoneNumber', None)
        sent_time = arrow.utcnow()
        delay_min = int(request.form.get('delay', None))
        scheduled_time = sent_time.replace(minutes=+delay_min)
        scheduled_time = scheduled_time.datetime
        schedule_call.apply_async(args=[phone_number], eta=scheduled_time)

        return jsonify({'message': 'Call incoming!'})

class ResourceOutboundCall(MethodView):
    def post(self):
        if validate_signature():
            resp = twiml.Response()
            resp.say("Hello! Welcome to the telephone fizz buzz game!")
            with resp.gather(timeout=10, finishOnKey="*", action="https://schedule-fizzbuzz.herokuapp.com/handlekey", method="POST") as g:
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
        digits_pressed = request.values.get('Digits', None)
        resp = twiml.Response()
        resp.say("You've pressed" + digits_pressed)
        resp.say("Now, let's start our fizz buzz game!")
        resp = self.get_fizz_buzz(resp, digits_pressed)
        resp.say("That's it! Thanks for playing! Good bye!")
        return str(resp)

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

