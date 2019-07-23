from flask import Flask, request
from flask_pymongo import PyMongo
from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import time
import threading
import os

app = Flask(__name__)

# connect database
# app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/database_predictions"
# mongo = PyMongo(app)

@app.route('/home', methods =['GET','POST'])
def home():
    return render_template('home.html')

@app.route("/home", methods=['GET'])
def home_page():
    return render_template("home.html")


@app.route('/resume', methods=['GET','POST'])
def nlp():
    return render_template('resume.html')


@app.route('/form_example', methods=['GET'])
def form_display():
    return ''' <form action="/string_reverse" method="POST">
                <input type="text" name="some_string" />
                <input type="submit" />
               </form>
             '''

@app.route('/string_reverse', methods=['POST'])
def reverse_string():
    text = str(request.form['some_string'])
    reversed_string = text[-1::-1]
    return ''' output: {}  '''.format(reversed_string)






if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080, debug=True)
        