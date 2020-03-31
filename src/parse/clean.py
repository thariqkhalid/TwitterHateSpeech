from parse_csv import *
import string, re
import nltk
nltk.download('wordnet')
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
nltk.download('punkt')
from nltk.corpus import stopwords
import spacy

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


def clean_tweet(tweet):

    # to remove http(s) url links
    text = re.sub('(https|http).*', '', tweet)
    # to remove other url links
    text = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", tweet)

    # to remove mentions
    text = re.sub(r"\. ", "<eos> ", tweet)  # replace the full stops with <eos> to save the full stops from the below re
    text = ' '.join(re.sub('(@[A-Za-z0-9_]*)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', '', text).split())
    text = re.sub(r"<eos>", ".", text)  # now convert back the <eos> to full stops
    #print(text)
    #print('\n')

    # split into words
    tokens = word_tokenize(text)

    # convert to lower case
    tokens = [w.lower() for w in tokens]

    # remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]

    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]

    # filter out stop words
    stop_words = set(stopwords.words('english'))
    # print(stop_words)
    words = [w for w in words if not w in stop_words]
    #print(words[:100])
    #print('\n')

    # stemming of words
    porter = PorterStemmer()
    stemmed_words = [porter.stem(word) for word in words]
    #print(stemmed_words)

    # lemmatization
    # Init the Wordnet Lemmatizer
    lemmatizer = WordNetLemmatizer()

    # Lemmatize list of words and join
    lemmatized_output = ' '.join([lemmatizer.lemmatize(w) for w in stemmed_words])
    clean_tweet = lemmatized_output
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
import sys
from textblob import TextBlob

a = "Yet another reason why India needs CAA: \n\nHindus Beaten by Pakistani Police for Hoisting Saffron Flag in Their Own Home"  # incorrect spelling
print("original text: " + str(a))

b = TextBlob(a)

# prints the corrected spelling
print("corrected text: " + str(b.correct()))