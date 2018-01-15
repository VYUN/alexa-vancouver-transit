import logging
import requests
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")

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
	time = data[0]["Schedules"][0]["ExpectedLeaveTime"]
	msg = "Next bus is at {}".format(time)
	return statement (msg)

if __name__ == '__main__':
    app.run(debug=True)


