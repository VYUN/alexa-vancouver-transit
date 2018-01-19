import logging
import requests
import json
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/bus")

log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG) 
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def launch():
	return statement ("Welcome to Alexa Vancouver Transit")

@ask.session_ended
def session_ended():
	log.debug("Session Ended")
	return "", 200

@ask.intent("NextBusIntent")
def next_bus(stop, route):
    if route:
        url = "http://api.translink.ca/rttiapi/v1/stops/" + stop + "/estimates?apikey=HM0OnI2DYHVUtHv28WZK&count=1&routeNo=" + route
    else:
        url = "http://api.translink.ca/rttiapi/v1/stops/" + stop + "/estimates?apikey=HM0OnI2DYHVUtHv28WZK&count=1"
    headers = {"Accept" : "application/json"}
    data = requests.get(url, headers=headers).json()
    time = data[0]["Schedules"][0]["ExpectedLeaveTime"].split(' ',1)[0] #Discard date
    destination = data[0]["Schedules"][0]["Destination"]
    msg = "The next bus is at {}, to {}".format(time, destination)
    return statement(msg)

@ask.intent("NextBusToIntent")
def next_bus_to(stop, destination):
    url = "http://api.translink.ca/rttiapi/v1/stops/" + stop + "/estimates?apikey=HM0OnI2DYHVUtHv28WZK&count=10"
    headers = {"Accept" : "application/json"}
    data = requests.get(url, headers=headers).json()
    jsonSchedule = data[0]["Schedules"]
    for schedule in jsonSchedule:
        if schedule["Destination"].lower() == destination.lower():
            time = schedule["ExpectedLeaveTime"].split(' ',1)[0]
            break
    msg = "The next bus to {} is at {}".format(destination, time)
    return statement(msg)

if __name__ == '__main__':
    app.run(debug=False)


