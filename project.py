#!/usr/bin/python
import requests
import time
import datetime
import RPi.GPIO as GPIO

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

#SW1 INPUT at GPIO pin #19
GPIO.setup(17,GPIO.IN)
#SW2 INPUT at GPIO pin #26
GPIO.setup(22,GPIO.IN)
#Capture Image OUTPUT at GPIO pin #20
GPIO.setup(20,GPIO.OUT)
#Send Emergency Alert OUTPUT at GPIO pin #21
GPIO.setup(21,GPIO.OUT)

i=0; n=100; delay=3;

while i<n:
	#Read status of switches and LEDs
	SW1=GPIO.input(17)
	SW2=GPIO.input(22)
	gLED=GPIO.input(20)
	rLED=GPIO.input(21)

	#Send JSON Request
	data = {'username': 'user', 'password': 'pass', 'SW1': SW1, 'SW2': SW2, 'gLED': gLED, 'rLED': rLED, 'SENDER': 'RPI'}
	res = requests.post("https://0254934.000webhostapp.com/scripts/sync_data.php", json=data)
	r = res.json()

	#Get the TimeStamp
	ts = datetime.datetime.now()
	print "==============Server Response at " + str(ts) + "=============="
	if r['success']==1:
		print "+++++Server request successful: "
		if gLED!=r['gLED']:
			print "Changing Green LED status as requested by the server:"
			if r['gLED']==1:
				GPIO.output(20,GPIO.HIGH)
			else:
				GPIO.output(20,GPIO.LOW)
		if rLED!=r['rLED']:
			print "Changing Red LED status as requested by the server:"
			if r['rLED']==1:
				GPIO.output(21,GPIO.HIGH)
			else:
				GPIO.output(21,GPIO.LOW)

		print "The status of SW1 is " + str(r['SW1'])
		print "The status of SW2 is " + str(r['SW2'])
		print "The status of GREEN LED is " + str(r['gLED'])
		print "The status of RED LED is " + str(r['rLED'])
	else:
		print ">>>>> Server request failed - Error #" + str(r['error'])
	#wait for delay seconds before sending another request
	time.sleep(delay)
	i+=1

GPIO.cleanup()

