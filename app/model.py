import numpy as np
import pandas as pd
from pandas import Series, DataFrame

import pickle

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier

def perdicet_category(text_words):

    categories_multi_lable = [
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

    predictions = dict((label,0) for label in categories_multi_lable)

    for category in categories_multi_lable:
        
        # open model file
        model_file_name = "./multi_models/mulitlablemodel_" + category +".pickle"

        model = open(model_file_name, "rb") 
        LogReg_pipeline_category = pickle.load(model)

        # calculating prediction
        perdicet_category_values = LogReg_pipeline_category.predict(text_words)

        predictions[category] = perdicet_category_values

    return prediction