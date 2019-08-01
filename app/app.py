from flask import Flask, flash, request, render_template, jsonify, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
import pandas as pd
import numpy as np
import time, threading, os, gensim, logging, json
from data_clean import cleanHtml, cleanPunc, keepAlpha, removeStopWords, stemming, clean_date
from model import tf_idf, perdicet_category
from pymongo import MongoClient
from bson import ObjectId
from werkzeug.utils import secure_filename
from flask import send_from_directory
from werkzeug import SharedDataMiddleware
from lda import preprocess

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


from inventory import find_random_genres, movie_genres

UPLOAD_FOLDER = '~/Project/Galavine/ResumeClassifier/app/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'doc', 'docx'])

app = Flask(__name__)
Bootstrap(app)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads':  app.config['UPLOAD_FOLDER']
})

model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './model/lda_simple_8743.model'))
dictionary_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './model/lda_dictionary'))

lda_model = gensim.models.LdaMulticore.load(model_path)
lda_dictionary = gensim.corpora.dictionary.Dictionary.load(dictionary_path)

# connect database
# app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/database_predictions"
# mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/v1.0/actor_sample/<string:genre>', methods=['GET'])
def api_actor_sample(genre):
    client = MongoClient()
    client = MongoClient('localhost', 27017)

    db = client.resumeclassifier
    collection = db.actor_labels

    genre_info = movie_genres[genre]

    match_object = {}

    match_object[genre_info['field_name']] = 1

    result = list(collection.aggregate([
        { "$match": match_object },
        { "$sample": { "size": 5 } }
    ]))

    client.close()
    return jsonify([JSONEncoder().encode(item) for item in result])

@app.route('/home', methods=['POST','GET'])
def home():
    if request.method=='POST':
        user_name = request.form['usr']
    else:
        user_name = ""
    return render_template('home.html', user_name=user_name, sample_movie_genres=find_random_genres(6))


@app.route('/multilabel', methods=['GET','POST'])
def multilabel():
    reminder = ''
    return render_template('multilabel_submit.html', reminder=reminder)

# results
@app.route('/multilabel_recommendations', methods=['GET','POST'])
def multilabel_recmomendations():
    errors=[]
    reminder = ''
    url = 'wait type'
    if request.method=='POST':
        # get url
        url = ''
        try:
            url = request.form['user_input_test']
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )

    if url != 'wait type' and url != 'Please input more than 250 words' and len(url) <= 250:
        reminder = 'Please input more than 250 words'
        return render_template('multilabel_submit.html', reminder1=reminder)
    else:
        data_raw = url

    data_raw = url

    test_data = clean_date(data_raw)

    data = tf_idf(test_data)

    predictions = perdicet_category(data)

    # predictions = {'url': '1' , 'b': '0', 'c': '1'} # for testing

    # return render_template('multilabel_recommendations.html', errors=errors, predictions=predictions)
    return render_template('multilabel_submit.html', errors=errors, predictions=predictions)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_from():
    if request.method == 'POST':
        # check if the post request has the file part
        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
        reminder = 'will upload'
        file = request.files['file']
        if file.filename == '':
            # flash('No file selected for uploading')
            # return redirect(request.url)
            reminder = 'No file selected for uploading'
            return render_template('multilabel_submit.html', reminder2=reminder)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            x = file.read()
            data_raw = x
            test_data = clean_date(data_raw)
            data = tf_idf(test_data)
            predictions = perdicet_category(data)
            # reminder = 'Loading'
            x = ''
            file.close()
            return render_template('multilabel_submit.html', predictions=predictions)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # flash('Loading')
            # return redirect(request.url)
        else:
            # flash('Allowed file types are txt, pdf, doc, docx')
            # return redirect(request.url)
            reminder = 'NAllowed file types are txt, pdf, doc, docx'
            return render_template('multilabel_submit.html', reminder2=reminder)

# temp
@app.route('/results_lda', methods=['GET','POST'])
def lda():
    return render_template('results_lda.html')

# @app.route('/recommendations', methods=['GET','POST'])
# def recmomendations():
#     return render_template('recommendations.html')

@app.route('/recommendations_lda', methods=['GET'])
def recommendations_lda():
    return render_template('recommendations_lda.html')

@app.route('/recommendations_lda', methods=['POST'])
def recommendations_lda_post():
    resume = request.form['resume']

    words_doc = preprocess(resume)

    bow_doc = lda_dictionary.doc2bow(words_doc)

    vector = lda_model[bow_doc]

    json_object = [{
        "topic_id": e[0],
        "score": str(e[1])
    } 
    for e in vector]

    app.logger.info('resume', vector)

    return jsonify({ 'result': json_object})


if __name__ == '__main__':

    
    app.config['SESSION_TYPE'] = 'filesystem'

    if ('USER' in  os.environ) and (os.environ['USER'] == 'ubuntu'):
        app.run(host='0.0.0.0', port=8088, debug=True)
    else:
        app.run(host='0.0.0.0', port=8080, debug=True)
        
