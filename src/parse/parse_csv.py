import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter, defaultdict

import os, sys

def get_proper_tweets(csvname):
    tweets_df = pd.read_csv(csvname)
    all_tweets = tweets_df[:190000]
    caa_tweets = all_tweets.tweet
    hashtags = all_tweets.hashtags
    date = all_tweets.date
    retweets_count = all_tweets.retweets_count
    likes_count = all_tweets.likes_count
    useful_tweets = list(zip(caa_tweets,date, hashtags, retweets_count, likes_count))
    return useful_tweets


''' This function is used to separate hindi and other tweets'''
def separate_hindi_other_tweets(tweets):
    etweets = []
    htweets = []

    for t, tweet_tup in enumerate(tweets):
        e_flag = 1
        tweet = tweet_tup[0]
        for c in tweet:
            if c == "\n":
                continue
            if ord(c) > 31 and ord(c) < 127:
                continue
            elif ord(c) > 2300 and ord(c) < 2400:  # hindi
                e_flag = 0
                htweets.append(tweet_tup)
                break
            else:
                continue
        if e_flag == 1:
            etweets.append(tweet_tup)

    return etweets, htweets


''' This function is used to separate english and other tweets'''
def separate_english_other_tweets(eng_uni_tweets):
    english_tweets = []
    other_tweets = []

    for t, etup in enumerate(eng_uni_tweets):
        e_flag = 1
        tweet = etup[0]
        for c in tweet:
            if c == "\n":
                continue
            if ord(c) > 31 and ord(c) < 250:
                continue
            elif ord(c) > 8200 and ord(c) < 8400:  # special punctuations
                continue
            elif ord(c) > 9000:  # smileys
                continue
            else:
                #             print(c, ord(c))
                e_flag = 0
                break
        if e_flag == 1:
            english_tweets.append(etup)
        else:
            other_tweets.append(etup)

    return english_tweets, other_tweets

def dump_frequency_dictionary(english_tweets):
    freqDict = dict()
    freq_file = open("frequency_dict.txt","w")

    for tweet in english_tweets:
        words = tweet[0].split()
        for word in words:
            if word not in freqDict:
                freqDict[word] = 1
            else:
                freqDict[word] += 1

    for k, v in freqDict.items():
        freq_file.write((k)+ "\t" + str(v) + "\n")

    freq_file.close()


if __name__ == "__main__":
    # parse the tweets to get the english unicode and then the english language
    # tweet_file = sys.argv[1]
    tweet_file = "/Users/thariq/Research/Cook/TwitterHateSpeech/tweets_till_0901.csv" #sys.argv[1]
    useful_tweets = get_proper_tweets(tweet_file) # send the filename from the command line at terminal
    eng_unicode_tweets, _ = separate_hindi_other_tweets(useful_tweets)
    english_tweets, _ = separate_english_other_tweets(eng_unicode_tweets)

    # let's dump the frequency dictionary into a file
    dump_frequency_dictionary(english_tweets)


