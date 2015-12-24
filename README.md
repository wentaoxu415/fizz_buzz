# Schedule Fizz Buzz
This is a web application created for Lendup's interview process.
Created in Flask with Twilio API, it plays fizz buzz with the input entered by the user.
To use the website in phase 4, visit https://schedule-fizzbuzz.herokuapp.com/

##Instruction 
1. To run the application in each phase, go into the corresponding directory and upload the files onto a Heroku server. 
2. In the environment, set the values for REDIS_URL, DATABASE_URL, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_NUMBER. 
3. Point your TWILIO to the url in which you are hosting your web application. 
4. Start a dyno and run the application. 

##Phase 1
    Created using Flask framework. Call the Twilio Number to play fizz buzz on your phone. 
##Phase 2
    Created using Flask framework with a web interface. Visit the website and enter your number to play fizz buzz on your phone. 
##Phase 3
    Created using Flask framework and Celery to support delay call. Visit the website and enter your number and delay minutes to play fizz buzz on your phone. 
##Phase 4
    Created using Flask framework, Celery, and Postgres to store and display the past call. Visit the website and enter your number and delay minutes to play fizz buzz on your phone. Click on "Listen" to hear the recording of fizz buzz from the past phone calls. 