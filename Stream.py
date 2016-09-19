
import tweepy
import json
import random
import sys
import time
import datetime
from functools import wraps
from pythonosc import osc_message_builder
from pythonosc import udp_client


#Setup tweepy to authenticate with Twitter

TWITTER_APP_KEY="GuMij7FSXlmfBWFOigRmfdo01"
TWITTER_APP_SECRET="hJFucjwjMLrz1oQTMNRct7xWgvb17pEwcG2yn2aUudRU4goIWd"
TWITTER_KEY="763539557405130752-cZJNgZSsDYFyWHLrS3Vp4xk930dlXpd"
TWITTER_SECRET= "dbg6BhjfqA6Kt4qnQRGYyKi3kY1xB8NW40A9DuwrDyY7W"

auth = tweepy.OAuthHandler(TWITTER_APP_KEY, TWITTER_APP_SECRET)
auth.set_access_token(TWITTER_KEY, TWITTER_SECRET)

#Create an API object to pull data from Twitter – we’ll pass in the authentication:
api = tweepy.API(auth)
RT=0
tweets=0
RTcharacters=0
tweetscharacters=0



class StreamListener(tweepy.StreamListener):

    # Create a listener that prints the text of any tweet that comes from the Twitter API - All of them


    # Handle errors .If it is 420, rate limited, we’ll want to disconnect; otherwise, we’ll keep going
    def on_error(self, status_code):

        if status_code == 420:
            return False


    def on_status(self, status):
        global RT,tweets,RTcharacters,tweetscharacters

        #tweetscharacters = float(len(status.text)) #Number of characters per tweet
        tweets = float(tweets+1) #Number of tweets


        #Sending OSC message each time a tweet is send...
        client = udp_client.UDPClient('localhost', 6448)
        msg = osc_message_builder.OscMessageBuilder(address="/wek/inputs")


        print(status.text) #print the content of the tweet
        msg.add_arg(tweets)  # OSC sends the number of characters per tweet
        msg = msg.build()
        client.send(msg)

# Create an instance of our StreamListener class
stream_listener = StreamListener()

# Instance of the tweepy Stream class, which will stream the tweets
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

# Start streaming tweets by calling the filter method
first = str(input("Please digit your search term: "))
stream.filter(track=[first])




