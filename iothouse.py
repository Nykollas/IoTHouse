rom tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import API
import time
import serial
import random as rnd
from datetime import datetime
access_token = "2721731623-NdFKS3Ap16mposU63myRdrHRfabpsz3wIHVAi24"
access_token_secret = "Gq7VeXT0kGN3jNiN3yYcjDLbFmZj2orFPZAljrTArAsYq"
consumer_key =  "gcw1yVdrqeH74STtwP51EoQvy"
consumer_secret = "ruuvKUtumnEkgQS6yW7jDExuqUGQBOzmZMAT5jpQTFGc5c0jaO"
ser = serial.Serial("COM5", 9600)


def getLGP():
    ser.write(b'1')
    return float(ser.readline().decode())

def getStatus():
    status = api.user_timeline("@Nyykkko")
    words = status[0].text.split()
    return words[0], words[1]


def checkLGP():
    lgpValue = getLGP()

    if(lgpValue >= 5000):
        api.update_status(messagesLGP['1'].format(lgpValue, rnd.randint(0,10000)))
    else:
        api.update_status(messagesLGP['0'].format(lgpValue,rnd.randint(0,10000)))

opt = {'LGPValue':checkLGP }

messagesLGP =  {"1":"A casa corre risco de incendio LGP: {0} cod: {1}","0":"A quantidade de LGP esta ok LGP:{0} cod: {1}"}


if __name__ == '__main__':
    auth =  OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth)
    print("Rodando\n")
    while(1):
        ret, option = getStatus()
        if(ret == "#iothouseIF"):
            print("OK")
            opt[option]()
        else:
            print("Not OK")
        time.sleep(5)

