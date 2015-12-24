from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import url_for

from twilio import twiml
from twilio.util import RequestValidator
from twilio.rest import TwilioRestClient
import os

# Declare and configure application
app = Flask(__name__, static_url_path='/static')

# Route for Click to Call demo page.
@app.route('/')
def index():
    return render_template('index.html',
                           configuration_error=None)


# Voice Request URL
@app.route('/call', methods=['POST'])
def call():
    
    # Credentials
    twilio_account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    twilio_auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    twilio_number = os.environ.get("TWILIO_NUMBER")
    print twilio_account_sid, twilio_auth_token, twilio_number
    validator = RequestValidator(twilio_auth_token)

    first_request = True
    
    # Get phone number we need to call
    phone_number = request.form.get('phoneNumber', None)
    

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
        if not validator.validate(my_url, params, twilio_signature):
            abort(401)
    
    
    
    try:
        twilio_client = TwilioRestClient(twilio_account_sid, twilio_auth_token)
    except Exception as e:
        msg = 'Missing configuration variable: {0}'.format(e)
        return jsonify({'error': msg})

    try:
        twilio_client.calls.create(from_=twilio_number,
                                   to=phone_number,
                                   url=url_for('.outbound',
                                               _external=True))
    except Exception as e:
        app.logger.error(e)
        return jsonify({'error': str(e)})

    return jsonify({'message': 'Call incoming!'})


@app.route('/outbound', methods=['POST'])
def outbound():
    resp = twiml.Response()
    resp.say("Hello! Welcome to the telephone fizz buzz game!")
    
    with resp.gather(timeout=10, finishOnKey="*", action="/handle-key", method="POST") as g:
        g.say("Please enter your number and then press star.")
    
 
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

