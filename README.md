# SoccerRefCalendar

## Technologies
1. Python 3.8
2. MechanicalSoup for web scraping
3. Google APIs for calendar access/updates
4. AWS Lambda
5. AWS Lambda Layer

6. AWS Eventbridge (Cloudwatch Events)
7. AWS Lambda Destination that is another AWS Lambda Function
8. Pushbullet notifications

## Automate the boring stuff
There are not too many other things as boring as manually adding a constant stream of events
into Google Calendar.  Manually it is 6 clicks and some typing, or loading a .ics is 6 clicks
after you obtain the file.
For me, this stream of events comes from a number of web sites dedicated to managing soccer
(futbol) referees.  Each week I get anywhere from 4 to 12 events to put into my calendar from:
* [mysoccerleague.com](https://mysoccerleague.com)
* [gameofficials.net](https://gameofficials.net)
* [gotsoccer.com](https://gotsoccer.com)
* [arbiter.com](https://arbiter.com)

## Some assembly required

You have to run this the first time and then authorize Google to allow access.  It's easy, and it will create a key.json file.  Please refer to Googles documentation at [the Google Python API Quickstart](https://developers.google.com/google-apps/calendar/quickstart/python) for details

## To run it locally
```bash
python -m venv venv
. venv/bin/activate
pip3 install mechanicalsoup
pip3 install httplib2
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip3 install --upgrade oauth2client
pip3 install icalendar
```

Uncomment the last line in main.py, then
```bash
python3 main.py
```
Or run it under your favorite debugger.

## The AWS Lambda Deployment


## The AWS Lambda Layer
You could package up everything into a single zip file and create your lambda function from it.  That is not as nice an experience because you won't 
have the online IDE available.  So instead, take the site-packages from your virtual environment and use that to create a layer.  If you have been following along, you might remember we created our virtual environment in the venv directory.  To create the lambda layer:

1) cd into the venv directory
```bash
cd venv/lib64/python3.8/site-packages
```
2) Remove all the __pycache__ directories
```bash
find . -name __pycache__ | xargs rm -rf
```
When an AWS Lambda for python has a layer attached, it expects the directory structure to look like:
python/lib/python3.8/site-packages/<packages>, so let's set that up:
```bash
mkdir -p python/lib/python3.8/site-packages
```

Populuate this new directory with the contents of the virtual environment's site-packages:
```bash
cp -r * python/lib/python3.8/site-packages
```
Yeah, yeah, can't copy python into itself.  That's really what we want.

Create a zip file:
```bash
zip -r lambda.layer.zip python/*
```

When we get around to setting up our lambda function via the AWS console, we will need lambda.layer.zip.

This program expects your usernames and passwords for each of the websites to be environment variables.  Don't forget to set these up in the AWS Lambda Configuration.

