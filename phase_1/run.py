from flask import Flask, request, redirect

from twilio import twiml
from twilio.util import RequestValidator

import os

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
    """Respond to incoming requests."""

    resp = twiml.Response()
    first_request = True
    twilio_account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    twilio_auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    twilio_number = os.environ.get("TWILIO_NUMBER")

    validator = RequestValidator(twilio_auth_token)
    
    if 'X-Twilio-Signature' not in request.headers:        
        if first_request:
            first_request = False
        else:
            abort(401)
    else:         
        my_url = request.url
        if my_url.startswith('http://'):
            my_url = my_url.replace("http", "https")
        
        params = request.form
        
        twilio_signature = request.headers['X-Twilio-Signature']
        
        if validator.validate(my_url, params, twilio_signature):
            resp.say("Hello! Welcome to the telephone fizz buzz game!")
            with resp.gather(timeout=10, finishOnKey="*", action="/handle-key", method="POST") as g:
                g.say("Please enter your number and then press star.")
        else: 
            abort(401)
            
    return str(resp)
        

@app.route("/handle-key", methods=['GET', 'POST'])
def handle_key():
    # Get digits pressed by the caller
    digits_pressed = request.values.get('Digits', None)
    
    resp = twiml.Response()
    resp.say("You've pressed " + digits_pressed)
    resp.say("Now, let's start our fizz buzz game!")
    resp = get_fizz_buss(resp, digits_pressed)
    resp.say("That's it! Thanks for playing! Good bye!")
    return str(resp)

def get_fizz_buss(resp, digits):
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

if __name__ == "__main__":
    app.run(debug=False)