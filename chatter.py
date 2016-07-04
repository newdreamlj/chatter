#!/usr/bin/python2.7
#coding=utf-8
import paho.mqtt.client as mqtt
import random
import time
import getpass
import sys

time_tic = 0

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
	result = {
		0: "Connection successful",
		1: "Connection refused - incorrect protocol version",
		2: "Connection refused - invalid client identifier ",
		3: "Connection refused - server unavailable ",
		4: "Connection refused - bad username or password ",
		5: "Connection refused - not authorised "
	}

	print(result[rc])
	if rc == 0:
		print("Have fun!")	
	else:
		print("Loggin failed.. Run it again!")
		sys.exit()	

	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	pass

def on_disconnect(client, obj, rc):       
	client.reconnect()

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	text = str(msg.payload).decode('base64')
	if text.startswith(userdata):   # this could be a problem
		pass
	else:
		#INSERT_ONE_LINE = '\x1b[1L'
		#CURSOR_UP_ONE = '\x1b[1A'
		#ERASE_LINE = ''#'\x1b[2K'
		#print(INSERT_ONE_LINE+CURSOR_UP_ONE + ERASE_LINE)
		print('\n'+str(msg.payload).decode('base64')+'\x07')
		#CURSOR_DOWN_ONE = '\x1b[1B'
		sys.stdout.write(userdata+": ")
		sys.stdout.flush()
		# print('\x1b[1C\x1b[1D')


#def on_timer():
#	global time_tic


client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

user = raw_input("Username: ")
# psw = getpass.getpass("Password: \n")
# towhom = raw_input("想跟谁聊天?\n")

client.user_data_set(user)
client.username_pw_set(user)
client.connect("52.76.99.49", 1883)

# timer = threading.Timer(1,on_timer)
# timer.start()

client.subscribe("public/chatter", 1)
client.loop_start()
time.sleep(1)
print("\n")

while True:
	# print("PUB "+str(time_tic))
	text = raw_input(user+": ");

	if text == "exit":
		sys.exit()
	if text != "":
		client.publish("public/chatter", (user+": "+text).encode('base64','strict'))

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

