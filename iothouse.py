
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import API
import time
import serial
# -*- coding: utf-8 -*-
import codecs
import random as rnd
import threading 
from datetime import datetime
access_token = ""
access_token_secret = ""
consumer_key =  ""
consumer_secret = ""
ser = serial.Serial("COM5", 9600)

def getLGP():
	ser.write(b'1')
	a = float(ser.readline().decode())
	return a

def getRain():
	ser.write(b'2')
	a = float(ser.readline().decode())
	return a

def getStatus():
	status = api.user_timeline("@Nyykkko")
	words = status[0].text.split()
	return words[0]
def justGetLGP():
	ser.write(b'1')
	ser.readline()

messagesLGP =  {"1":"A casa corre risco de incendio!!!\n LGP: {0} cod: {1}", "0":"Dados da casa:\nLGP:{0}\nSensor de chuva:{2} cod: {1}","2":"Esta chovendo!! cod: {0}","3":"Parou de chover!! cod: {0}"}

if __name__ == '__main__':
	auth =  OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = API(auth)
	print("Rodando\n")
	time.sleep(5)
	t = 0
	h = 0
	while(1):
		justGetLGP()
		lgpValue = getLGP()	
		rainValue = getRain()
		print("LGPValue: {0} \t RainValue: {1}".format(lgpValue,rainValue))
		ret = getStatus()
		if(ret == "#iothouseIF"):
			print("OK")
			api.update_status(messagesLGP['0'].format(lgpValue, rnd.randint(0,10000), rainValue))
		else:
			print("Not OK")
		if(lgpValue >= 5000 or lgpValue < 0):
			api.update_status(messagesLGP['1'].format(lgpValue, rnd.randint(0,10000)))

		if(rainValue < 700):
			if time.time() - t > 1800:
				h = 1
				api.update_status(messagesLGP['2'].format(rnd.randint(0,10000)))
				t = time.time()
		elif(h == 1 and rainValue >= 700):
				h=0
				api.update_status(messagesLGP['3'].format(rnd.randint(0,10000)))
