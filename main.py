# This is a sample Python script.
import random
import sys
from collections import defaultdict, Counter
import tweepy
import time
import numpy as np
import threading
from os import listdir
from os.path import isfile, join



sys.path.append(".")

from markovChain import MarkovChain
from tweetAnalysis import TweetCleaner


# leggere i tweet e salvarli da parte, dopo averli ripuliti
#  dare in pasto il file di testo alla catena
# TODO: stampare il messaggio (per vedere se credibile), se risultano credibili metterli su twitter
#####################################
# Nice to have
# TODO: postare immagini, meglio se generate un po' a caso o prese da internet
# TODO: mettere like a gente che la pensa come il bot
# TODO: followare gente che la pensa come il bot
# TODO: risposta in automatico ai messaggi, magari mandandoli a quel paese dicendogli "scusa ma non ho tempo da perdere, voto salvini"

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
loginData = open('login_data.txt').read()
CONSUMER_KEY = loginData[0]
CONSUMER_SECRET = loginData[1]
ACCESS_KEY = loginData[2]
ACCESS_SECRET = loginData[3]
#fixme check if this works

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

TWEETS = 'tweets.txt'
tweets_path = './src/' + TWEETS
print('...')
twitter_API = tweepy.API(auth)


# 2 get user's name
# user= twitter_API.get_user('frankmatano')
# print('locazione: '+str(user.location)+' id:'+str(user.id)+' desc:'+str(user.description)+' nome:'+str(user.screen_name))

# 2 search stuff
#this makes the tweets readable
t = TweetCleaner()
#gets trends
trends = twitter_API.trends_place(id = 23424853)
trendList = []
for value in trends:
    for trend in value['trends']:
        trendList.append(trend['name'])
del trendList[9:]
print(trendList)
#picks a random query from trends
query = random.choice(trendList)
print('Query '+query)
users_id = set()
for query in trendList:
    for tweet in twitter_API.search(q=query,lang='it',result_type='recent',count=100,  tweet_mode="extended"):
        tweetText = tweet.full_text
        try:
            if tweet.retweeted_status:
                tweetText = tweet.retweeted_status.full_text
        except:
             pass

        finally:
            users_id.add(tweet.user.id)
            tweetText = t.skim(tweetText)
            print('SKIMMED: ' + tweetText)
        with open(tweets_path,'a',encoding='utf-16') as f:
            f.write(tweetText+'\n')
        time.sleep(2)
#fixme status code = 431
for user in users_id:
    for tweet in twitter_API.user_timeline(user_id = users_id,exclude_replies = 'true', include_rts='false'):
        tweetText = tweet.full_text
        try:
            if tweet.retweeted_status:
                tweetText = tweet.retweeted_status.full_text
        except:
            pass

        finally:
            tweetText = t.skim(tweetText)
            print('SKIMMED: ' + tweetText)
        with open(tweets_path, 'a', encoding='utf-16') as f:
            f.write(tweetText + '\n')
        time.sleep(2)




# 2 like and follow respectly stuff and people
# twitter_API.create_friendship(screen_name='niccothepug')
# for tweets in twitter_API.user_timeline(screen_name='niccothepug',count=3):
# print(str(tweets.user.name)+'\'s '+str(tweets.id)+' '+str(tweets.text))
# twitter_API.create_favorite(tweets.id)


###############################################################################################
# markov chain
 #<-- absolute dir the script is in
#folder = '/src'
#tmp_path = os.path.join(script_dir, folder)
#print(script_dir)
rel_path = {f for f in listdir('./src') if isfile(join('./src', f))}
#for files in rel_path:
    #src_files = os.path.join(tmp_path, files)
#print(src_files)
print(rel_path)
#chain = MarkovChain(rel_path)
#chain.loadAnalyzeCorpus()
#tic = time.perf_counter()
#for i in range(4):
    #print(str(chain.generateSentence())+'\n')
#toc = time.perf_counter()
#print(f'Real time: {toc-tic:0.4f} seconds')

