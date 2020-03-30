from parse_csv import *
import re

# create a global dictionary
dict_words = []
NON_ENGLISH_WORDS = 0.2

def load_dictionary():
    dictionary_file = open("./dictionary","r").readlines()
    dict_words = [w.strip().lower() for w in dictionary_file]
    return dict_words


# for deciding whether a tweet is english or not, lets define a threshold which is the percentage of english words
def english_or_not(tweet):
    print("Checking english tweet")
    words = tweet.split()
    non_eng_words = 0

    for w in words:
        if w.lower() not in dict_words:
            non_eng_words += 1
            print(w)

    print("Number of non english words ", non_eng_words )

    if (non_eng_words*0.1/len(words)) < NON_ENGLISH_WORDS :
        return False
    else:
        return True


def clean_url_mentions(tweet):
    # first let's replace the full stops with <eos>. This will help us to save the full stops from the below monster regular expression :)
    clean_tweet = re.sub(r"\. ", "<eos> ", tweet)
    clean_tweet = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))'''," ", clean_tweet)
    clean_tweet = re.sub(r"<eos>", ".", clean_tweet) # now convert back the <eos> to full stops
    return clean_tweet


if __name__ == "__main__":
    dict_words = load_dictionary()
    test_tweet_cleaning = "Yet another reason why India needs #CAA: \n\nHindus Beaten by Pakistani Police for Hoisting Saffron Flag in Their Own Home. " \
                 "Video Published to Cower Other Hindus into Submission!\n\n https://www.youtube.com/watch?v=lTQxDeBmCyI\xa0…\n"

    test_tweet_english1 = "Yeh hamarra haq hai"
    test_tweet_english2 = "This is an english test tweet witth spelling mistake"

    # test the clean function @Enaas
    clean_tweet = clean_url_mentions(test_tweet_cleaning)
    print(clean_tweet)

    # test the english dictionary lookup function @Fathma
    res = english_or_not(test_tweet_english2)
    if res:
        print("English tweet")
    else:
        print("Not an english tweet")

