from flask import Flask, request, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)

def get_restricted_df(price,item_index,range):
    try:
        nums = range.split('-')
        min = int(nums[0])
        max = int(nums[1])
    except:
        min = int(range) -50
        max = min + 50
    restricted = df.copy()
    restricted = restricted[restricted['sale_price'] >= min]
    restricted = restricted[restricted['sale_price'] < max]
    return restricted

@app.route('/', methods =['GET','POST'])
def index():
    return render_template('home.html')

@app.route('/home', methods =['GET','POST'])
def home():
    return render_template('home.html')

@app.route('/nlp', methods=['GET','POST'])
def nlp():
    return render_template('resume.html')

@app.route('/neural_net', methods=['GET','POST'])
def neural_net():
    choices = np.random.choice(images.index,5,replace=False)
    return render_template('neural_net.html',images=images,choices=choices)

@app.route('/nlp_recs', methods=['GET','POST'])
def nlp_recs():
    try:
        item_index= int(request.form['index'])
        range = str(request.form['price'])
    except:
        item_index= int(request.args.get('index'))
        range = ''
    if range == '':
        cluster_label = df['prediction'].iloc[item_index]
        cluster_members = df[df['prediction'] == cluster_label]
        recs = np.random.choice(cluster_members.index, 5, replace = False)
        return render_template('nlp_recs.html',recs=recs,df=df,item_index=item_index)
    if range != '':
        price = df['sale_price'].iloc[item_index]
        restricted = get_restricted_df(price,item_index,range)
        cluster_label = df['prediction'].iloc[item_index]
        cluster_members = restricted[restricted['prediction'] == cluster_label]
        if len(cluster_members) >= 5:
            recs = np.random.choice(cluster_members.index, 5, replace = False)
        elif len(cluster_members) != 0:
            recs = np.random.choice(cluster_members.index, len(cluster_members), replace = False)
        else:
            recs = []
        return render_template('nlp_recs.html',recs=recs,df=df,item_index=item_index)

@app.route('/cnn_recs', methods=['GET','POST'])
def cnn_recs():
    try:
        item_index= int(request.form['image'])
    except:
        item_index= int(request.args.get('image'))
    cluster_label = images['label'].iloc[item_index]
    cluster_members = images[images['label'] == cluster_label]
    cluster_members.drop(item_index,axis=0,inplace=True)
    recs = np.random.choice(cluster_members.index, 4, replace = False)
    recs = np.append(recs,np.random.choice(images.index))
    return render_template('cnn_recs.html',item_index=item_index,recs=recs,images=images)

if  __name__ == '__main__':
    df = pd.read_csv('s3a://capstone-3/data/spark_model.csv')
    images = pd.read_csv('s3a://capstone-3/data/images_and_labels5.csv')

    app.run(host='0.0.0.0',port=8080, debug=True, threaded=True)
