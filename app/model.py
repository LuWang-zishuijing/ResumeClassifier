import numpy as np
import pandas as pd
from pandas import Series, DataFrame

import pickle, os

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier

vectorizer_file_name = os.path.abspath(os.path.join(os.path.dirname(__file__), "./multi_models/vectorizer.pickle"))
train_filr_name = os.path.abspath(os.path.join(os.path.dirname(__file__), "./multi_models/train_web.pickle"))

vectorizer_uppickle = open(vectorizer_file_name, "rb") 
vectorizer_for_text = pickle.load(vectorizer_uppickle)
vectorizer_uppickle.close()

x_uppickle = open(train_filr_name, "rb") 
x_data = pickle.load(x_uppickle)
x_uppickle.close()

LogReg_pipeline = Pipeline([
    ('clf', OneVsRestClassifier(LogisticRegression(solver='sag'), n_jobs=-1)),
])

y = pd.read_csv('./multi_models/y_true.csv')

def tf_idf(test_data):

    vectorizer_for_text.fit(x_data)
    vectorizer_for_text.fit(test_data)

    x =  vectorizer_for_text.transform(x_data)
    data = vectorizer_for_text.transform(test_data)

    return x, data

def perdicet_category(data):

    x = data[0]
    test = data[1]

    # print(x.shape, test.shape)

    categories_multi_label = [
    'Adventure',
    'Romance',
    'History',
    'Crime',
    'Fantasy',
    'Horror',
    'Mystery',
    'Sci-Fi',
    'Thriller',
    'Action',
    'War',
    'Animation',
    'Comedy',
    'Biography',
    'Sport',
    'Musical',
    'Music',
    'Family',
    'Drama']


    predictions = dict((label,0) for label in categories_multi_label)

    for category in categories_multi_label:
        # Training logistic regression model on train data
        LogReg_pipeline.fit(x, y[category])
        
        # calculating test accuracy
        predictions[category] = LogReg_pipeline.predict(test)

    return predictions