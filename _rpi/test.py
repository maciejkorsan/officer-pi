#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, json
from azure.servicebus import ServiceBusService, Message, Queue
from threading import Event, Thread
import requests, random

def call_repeatedly(interval, func, *args):
    stopped = Event()
    def loop():
        while not stopped.wait(interval): # the first call is in `interval` secs
            func(*args)
    Thread(target=loop).start()    
    return stopped.set

def sendMessage(data):
	text = data['Text'];
	channel = data['Channel_Name']
	icon = ""

	if text == "popek":
		text = "*Popuś graj!* \n"
		text += random.choice(list(open('fun/gang.txt')))
		text += random.choice(list(open('fun/gang.txt')))
		text += random.choice(list(open('fun/gang.txt')))
		text += random.choice(list(open('fun/gang.txt')))
		icon = "http://tibiopedia.pl/images/static/avatars/Popek%20Monstera50bcd8.jpeg"

	if text == "joke":
		joke = requests.get("http://tambal.azurewebsites.net/joke/random")  
		joke = json.loads(joke.text) 
		text = ":bread: "+joke['joke'] 



	payload = {
		"text": text,
		"username": "officer-pi",
		"icon_emoji": ":cop:",
		"channel": "#"+channel
	}

	if icon != "":
		payload = {
			"text": text,
			"username": "KRÓL ALBANII",
			"icon_url": icon,
			"channel": "#"+channel
		}

	req = requests.post("", json.dumps(payload), headers={'content-type': 'application/json'})
	print(req.status_code, req.reason)

def getCommand(bs):
	msg = bs.receive_queue_message('officer', peek_lock=False) 
	response = msg.body
	if msg.body is not None:
		indexStart = response.index("{")
		response = response[indexStart:]
		response = "".join([response.rsplit("}" , 1)[0] , "}"]) 
		print response
		parsed = json.loads(response)
		print parsed 
		sendMessage(parsed) 
	else:
		print "Nihil novi"



bus_service = ServiceBusService(
    service_namespace='',
    shared_access_key_name='',
    shared_access_key_value='')

 
cancel_future_calls = call_repeatedly(5, getCommand, bus_service)