import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import re
import sys
import warnings
from sklearn.feature_extraction.text import TfidfVectorizer

if not sys.warnoptions:
    warnings.simplefilter("ignore")

# clean the word of html 
def cleanHtml(sentence):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', str(sentence))
    return cleantext

# clean the word of any punctuation
def cleanPunc(sentence): 
    cleaned = re.sub(r'[?|!|\'|"|#]',r'',sentence)
    cleaned = re.sub(r'[.|,|)|(|\|/]',r' ',cleaned)
    cleaned = cleaned.strip()
    cleaned = cleaned.replace("\n"," ")
    return cleaned

# clean the word of any special characters
def keepAlpha(sentence):
    alpha_sent = ""
    for word in sentence.split():
        alpha_word = re.sub('[^a-z A-Z]+', ' ', word)
        alpha_sent += alpha_word
        alpha_sent += " "
    alpha_sent = alpha_sent.strip()
    return alpha_sent

# clean the word of any special characters 
def removeStopWords(sentence):
    #set stope words
    stop_words = set(stopwords.words('english'))
    stop_words.update(['zero','one','two','three','four','five','six','seven','eight','nine','ten','may','also','across','among','beside','however','yet','within'])
    re_stop_words = re.compile(r"\b(" + "|".join(stop_words) + ")\\W", re.I)

    # global re_stop_words
    return re_stop_words.sub(" ", sentence)

# stemming word
def stemming(sentence):
    stemmer = SnowballStemmer("english")
    stemSentence = ""
    for word in sentence.split():
        stem = stemmer.stem(word)
        stemSentence += stem
        stemSentence += " "
    stemSentence = stemSentence.strip()
    return stemSentence

def clean_date(data_raw):
    test_data = pd.Series(np.array(data_raw.lower()))
    test_data = test_data.apply(cleanHtml)
    test_data = test_data.apply(cleanPunc)
    test_data = test_data.apply(keepAlpha)
    test_data = test_data.apply(removeStopWords)
    test_data = test_data.apply(stemming)
    return test_data