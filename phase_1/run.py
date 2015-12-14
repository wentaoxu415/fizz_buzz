from flask import Flask, request, redirect
import twilio.twiml
from twilio.util import RequestValidator


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
    """Respond to incoming requests."""

    resp = twilio.twiml.Response()
    
    # Replace with your own authorization token
    auth_token = '7b6c1a1b2e42c0dbb9204ed885cf5857' 
    validator = RequestValidator(auth_token)
    
    if 'X-Twilio-Signature' not in request.headers:        
        pass
    else:         
        my_url = 'https://still-escarpment-3259.herokuapp.com'
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
    
    resp = twilio.twiml.Response()
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
    app.run(debug=True)