import re          
import os  
import sys
import codecs
import shutil
from sklearn import feature_extraction  
# from sklearn.feature_extraction.text import TfidfTransformer  
# from sklearn.feature_extraction.text import CountVectorizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# get tf_idf
def tf_idf(corpus, max_features):

    # #method 1 CountVectorizer() + TfidfTransformer()
    # #Convert words into word frequency matrix elements a [i] [j] denotes the word frequency of j words.
    # vectorizer = CountVectorizer()
    # #count the tf-idf weight of each word.
    # transformer = TfidfTransformer()

    #method 2 TfidfVectorizer()
    vectorizer = TfidfVectorizer(max_features=max_features)

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


def kmeans(n_clusters, X, features):
    kmeans = KMeans(n_clusters)
    kmeans.fit(X)

    print("kmeans n_cluster=　{}, inertia: {}".format(n_clusters, kmeans.inertia_))


    top_centroids = kmeans.cluster_centers_.argsort()[:,-1:-21:-1]
    for num, centroid in enumerate(top_centroids):
        print("%d: %s" % (num, ", ".join(features[i] for i in centroid)))
    return kmeans, top_centroids


def plot_clusters(X, n_clusters, kmeans):
    tfidf_weight_all = X.toarray()

    tsne = TSNE(n_components=2)
    decomposition_data = tsne.fit_transform(tfidf_weight_all)
    fig = plt.figure(figsize=(10, 10))

    for color in range(0,n_clusters):
        label = []
        x = []
        y = []
        
        for i in range(len(kmeans.labels_)):
            if kmeans.labels_[i] == color:
                x.append(decomposition_data[i][0])
                y.append(decomposition_data[i][1])

        plt.scatter(x, y, label=color, marker="x")

    plt.legend()