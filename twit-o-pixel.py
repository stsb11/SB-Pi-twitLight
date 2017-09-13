#Import the necessary methods from tweepy library

# Install neopixel lib and tweepy first. 
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import time
import atexit
from neopixel import *

# Who are we looking for?
person = ['Trump is']

# LED strip configuration:
LED_COUNT      = 100      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# Intialize the library (must be called once before other functions).
strip.begin()
nextPixel = 0

#Variables that contains the user credentials to access Twitter API
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

def exit_handler():
    wipeIt()

atexit.register(exit_handler)

def wipeIt():
    for n in range(100):
        strip.setPixelColor(n, Color(0,0,0))

    strip.show()
    return

wipeIt()

#This is a basic listener that parses each tweet matching our keywords.
class StdOutListener(StreamListener):
    def on_data(self, data):
        # print data
        theTweet = json.loads(data)
        global nextPixel

        try:
            mainText = theTweet['text']
            if mainText.find("idiot") != -1 or mainText.find("bad") != -1 or mainText.find("evil") != -1:
                # Someone's called them an idiot. Turn a pixel red.
                strip.setPixelColor(nextPixel, Color(3,0,0))
                strip.show()
                nextPixel += 1
            elif mainText.find("smart") != -1 or mainText.find("good") != -1 or mainText.find("great") != -1:
                # Been called great. Pixel goes green.
                strip.setPixelColor(nextPixel, Color(0,3,0))
                strip.show()
                nextPixel += 1
            elif mainText.find("a-hole") != -1 or mainText.find("Dickens") != -1 or mainText.find("Flouting Jack") != -1:
                # Someone's called them a swear word. Turn a pixel blue.
                strip.setPixelColor(nextPixel, Color(0,0,3))
                strip.show()
                # print mainText
                nextPixel += 1
                
            if nextPixel >= 64:
                nextPixel = 0
                time.sleep(2)
                wipeIt()
        except:
            pass
        finally:    
            return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    # Look for keyword...
    stream.filter(track=person)


