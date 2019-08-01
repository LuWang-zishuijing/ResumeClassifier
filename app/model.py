import numpy as np
import pandas as pd
from pandas import Series, DataFrame

import pickle, os, sys

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier

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

model_file_names = [ "./model/LogReg_pipeline_" + label +".pickle" for label in categories_multi_label]

model_files = [os.path.abspath(os.path.join(os.path.dirname(__file__), model_file_name )) for model_file_name in model_file_names]

classifiers = []

for model_file in model_files:
    model_file_object = open(model_file, "rb") 
    classifier = pickle.load(model_file_object)
    model_file_object.close()

    classifiers.append(classifier)

def perdicet_category(data):
    predictions = dict((label,0) for label in categories_multi_label)

    index = 0
    for classifier in classifiers:
        prediction = classifier.predict(data)

        category = categories_multi_label[index]
        predictions[category] = prediction

        index = index + 1

    return predictions