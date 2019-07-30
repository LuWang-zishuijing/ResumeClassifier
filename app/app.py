from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
import pandas as pd
import numpy as np
import time
import threading
import os

app = Flask(__name__)
Bootstrap(app)

# connect database
# app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/database_predictions"
# mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home', methods =['GET','POST'])
def home():
    return render_template('home.html')

# method
@app.route('/multilabel', methods=['GET','POST'])
def multilabel():


    return render_template('multilabel_submit.html')

# temp
@app.route('/results_lda', methods=['GET','POST'])
def lda():
    return render_template('results_lda.html')

# @app.route('/resume', methods=['GET','POST'])
# def multilabel():
#     return render_template('resume.html')


# results
@app.route('/multilabel_recommendations', methods=['GET','POST'])
def recmomendations():
    predictions = [
        ['Adventure', '√'],
        ['Romance', ''],
        ['History', ''],
        ['Crime', ''],
        ['Fantasy', '√'],
        ['Horror', ''],
        ['Mystery', '√'],
        ['Sci-Fi', ''],
        ['Thriller', ''],
        ['Action', ''],
        ['War', ''],
        ['Animation', ''],
        ['Comedy', ''],
        ['Biography', ''],
        ['Sport', ''],
        ['Musical', ''],
        ['Music', ''],
        ['Family', ''],
        ['Drama', '']
        ]
    return render_template('multilabel_recommendations.html', predictions=predictions)

# @app.route('/recommendations', methods=['GET','POST'])
# def recmomendations():
#     return render_template('recommendations.html')


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080, debug=True)
        