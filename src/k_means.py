import re          
import os  
import sys
import codecs
import shutil
from sklearn import feature_extraction  
# from sklearn.feature_extraction.text import TfidfTransformer  
# from sklearn.feature_extraction.text import CountVectorizer

from sklearn.feature_extraction.text import TfidfVectorizer

# get tf_idf
def tf_idf(corpus, max_features):

    # #method 1 CountVectorizer() + TfidfTransformer()
    # #Convert words into word frequency matrix elements a [i] [j] denotes the word frequency of j words.
    # vectorizer = CountVectorizer()
    # #count the tf-idf weight of each word.
    # transformer = TfidfTransformer()

    #method 2 TfidfVectorizer()
    vectorizer = TfidfVectorizer(max_features=1000)

    #convert the text into a word frequency matrix.
    X = vectorizer.fit_transform(corpus)

    #Get all the words
    features = vectorizer.get_feature_names()
    
    # weight = X.toarray()

    # print('X(tf_idf): ')
    # print(X)

    # print('word features:')
    # print(word_features)
    return X, features


def kmeans(n_clusters):
    pass
