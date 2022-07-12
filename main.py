from flask import Flask,request,jsonify
import os
app = Flask(__name__)


# twitter start
import tweepy
consumer_key = os.environ.get('consumer_key')
consumer_secret = os.environ.get('consumer_secret')
access_token = os.environ.get('access_token')
access_token_secret = os.environ.get('access_token_secret')

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

def user_timeline(username):
    originalTweet = {}
    i = 0
    for tweet in tweepy.Cursor(api.user_timeline,screen_name=username,tweet_mode="extended").items(50):
        if tweet.full_text.startswith("@"):
            pass
        elif tweet.full_text.startswith("RT @"):
            pass
        else: 
            og = "https://twitter.com/twitter/statuses/"+ str(tweet.id)
            originalTweet[i] = og
            # originalTweet.append("https://twitter.com/twitter/statuses/" + str(tweet.id))
            #  originalTweet.append(tweet.full_text)
    # print(len(originalTweet))
        i+=1
    return originalTweet

# twitter end

# reddit
import praw
import requests
import random


folder_name = '../python/memes'
SUBREDDIT_NAME ='CodeGeass'
NO_OF_MEMES = 8
LIMIT = 15
VALID_SYM = 'abcdefghijklmnopqrstuvwxyz'

def image_check(link):
    """
    To check if the link is an img
    """

    IMG = {'jpg', 'jpeg', 'png'}
    for i in IMG:
        if link.endswith(i):
            return True

# create an application here - https://www.reddit.com/prefs/apps to get access to this
def memeSend():
    reddit = praw.Reddit(
            client_id = "IHCXgYzZpnu-r_-SrQrW_Q",
            client_secret = "Tkjj8gdhWnr-l8l7BxjzKI5gpNVXGw",
            username = 'Right-Buyer-7519', 
            user_agent = "meme-scr2",
)

    subreddit = reddit.subreddit(SUBREDDIT_NAME)
    lim = subreddit.top(limit=LIMIT)
    all_sub = [i for i in lim]

    memeList = {}

    submission = random.sample(all_sub, NO_OF_MEMES)
    for i in range(NO_OF_MEMES):
        url = submission[i].url
        title = submission[i].title
    
        for j in title:
            if j.lower() not in VALID_SYM:
                title = title.replace(j, '-')    
        # memeList.append(f'{url}')
        memeList[i] = f'{url}'

    return memeList
# twitter end


@app.route('/')
def hello_world():
    originalTweet = user_timeline("Cristiano")
    return originalTweet
    
            #  originalTweet.append(tweet.full_text)
    
@app.route('/memes')
def memes():
    meme = memeSend()
    return meme
