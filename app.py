import os
from flask import Flask, render_template, request
from flask import send_from_directory
import tweepy
from textblob import TextBlob
import numpy as np
from transformers import pipeline
from src.parse.clean import *
import pandas as pd
import xlwt
from xlwt import Workbook


app = Flask(__name__)

hashtags_file_path = 'uploads/hashtags_searched.txt'

#define variables for tweepy
consumer_key = 'bzV4SycWIbBRj7pY4rxt7AXAk' #enter consumer key
consumer_secret = 'aV1VOVmczfri8gm1W2NaDC5vN8FMq95fZSk5699uN94HEmm2hG' #enter consumer key secret
access_token = '47097480-yvqftLNat2WjpiqRPbudQ0DWW6R3NX7FKCFhKOP1H' #enter access token
access_token_secret = '2BLZi8dHUeuCWDONR2Q6olhV6knWwM2V8RrzJME3c3Y45' #enter access token secret


#setup twitter authentication
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)

# home page
@app.route('/')
def home():
   return render_template('index.html')


@app.route('/analyze', methods=['POST','GET'])
def analyzeTweet():
    # dict_words = load_dictionary()
    # print("dict_words: ", dict_words)
    # nlp = pipeline('sentiment-analysis')


    if request.method == 'GET':
        return render_template('index.html')
    else:
        hashtag = request.form['hashtag']
        f = open(hashtags_file_path,'a')
        if hashtag:
            tweets = []
            polaritylist = []
            subjectivitylist = []
            sentiments = []
            date_since = "2020-6-1"
            # tweets = api.search(hashtag, rpp=100, since_id=1, count=5000)
            tweets = tweepy.Cursor(api.search, q=hashtag, lang="en", since=date_since).items(100)
            wb = Workbook()
            s1 = wb.add_sheet('Sheet 1')

            s1.write(1, 0, 'SCREEN_NAME')
            s1.write(1, 1, 'TEXT')
            s1.write(1, 2, 'RETWEET_COUNT')
            s1.write(1, 3, 'POLARITY')

            # s1.write(1, 2, 'SENSITIVITY')
            # s1.write(1, 0, 'HASHTAGS')
            # s1.write(1, 0, 'ID')
            # s1.write(1, 0, 'ID')
            # s1.write(1, 0, 'ID')

            for t,tweet in enumerate(tweets):
                retweet_count = tweet.retweet_count

                if retweet_count < 20:
                    continue

                print(retweet_count)
                print(tweet.text)
                s1.write(t,0,user.screen_name)
                s1.write(t, 1, tweet.text)
                s1.write(t, 2, tweet.retweet_count)
                s1.write(t, 3, TextBlob(tweet.text).polarity)

                # s1.write(t, 2, tweet.possibly_sensitive)
                # s1.write(it, 0, tweet.id)

                # res = english_or_not(tweet.text)
                # if res:
                txt = tweet.text
                # txt = clean_tweet(tweet.text)
                # print(nlp(txt))
                # print(txt)
                if TextBlob(txt).polarity != 0.0 and TextBlob(txt).subjectivity != 0.0:
                    polaritylist.append(TextBlob(txt).polarity)
                    subjectivitylist.append(TextBlob(txt).subjectivity)

            wb.save('thariq.xls')
                    # print(TextBlob(txt).sentiment)


            if len(polaritylist) > 0 and len(subjectivitylist) > 0:
                polarity = round(np.mean(polaritylist),3)*100
                subjectivity = round(np.mean(subjectivitylist),3)*100
                sentiments = [polarity,subjectivity]
                f.write(hashtag + ' ' + '=> Polarity:' + str(polarity) + ' ' + 'Subjectivity:' + str(subjectivity) + '\n')
                f.close()
                return render_template('analyze.html', sentiments = sentiments, hashtag=hashtag)
            else:
                return render_template('analyze.html', error_message='No tweets found!')
        else:
            return render_template('analyze.html', error_message="Enter some hashtag!")



if __name__ == '__main__':
    app.run(debug=False,threaded=False)
