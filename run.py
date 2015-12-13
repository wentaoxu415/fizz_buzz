from flask import Flask, request, redirect
import twilio.twiml
 
app = Flask(__name__)
 
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming requests."""
    resp = twilio.twiml.Response()
    resp.say("Hello Monkey")
 
    with resp.gather(timeout=10, finishOnKey="*", action="/handle-key", method="POST") as g:
        g.say("Please enter your number and then press star.")

    return str(resp)
 
@app.route("/handle-key", methods=['GET', 'POST'])
def handle_key():
    digits_pressed = request.values.get('Digits', None)
    
    resp = twilio.twiml.Response()
    resp.say("You've pressed " + digits_pressed)
    resp.say("Now, let's start our fizz buzz game!")
    resp = get_fizz_buss(resp, digits_pressed)

    return str(resp)

def get_fizz_buss(resp, digits):
    
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