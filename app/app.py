from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
import pandas as pd
import numpy as np
import time
import threading
import os
from data_clean import cleanHtml, cleanPunc, keepAlpha, removeStopWords, stemming, tf_idf
from model import perdicet_category

app = Flask(__name__)
Bootstrap(app)

# connect database
# app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/database_predictions"
# mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home', methods=['POST','GET'])
def home():
    if request.method=='POST':
        user_name = request.form['usr']
        # user_name = 'TEMP'
        return render_template('home.html', user_name=user_name)
    else:
        return render_template('index.html')


@app.route('/multilabel', methods=['GET','POST'])
def multilabel():
    return render_template('multilabel_submit.html')

# results
@app.route('/multilabel_recommendations', methods=['GET','POST'])
def multilabel_recmomendations():

    errors=[]
    results = {}
    if request.method == "POST":
        # get url that the user has entered
        try:
            url = request.form['user_input_resume']
            r = requests.get(url)
            print(r.text)
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )

    # user_input_test = 'tyler tyler septemb bear rundgren juli york citi york resid london england occup year activ present spous royston langdon partner joaquin phoenix david gardner present children parent steven tyler bebe buell todd rundgren adopt legal relat tyler patern half sister chelsea tallarico patern half sister tallarico patern half brother foster brother warn page templat infobox person unknown paramet height messag show preview rundgren tyler bear rundgren juli american actress model portray arwen miel lord ring film trilog tyler begin career model later decid focus act film debut silent fall go achiev critic recognit role heavi empir record thing steal beauti appear film invent abbott armageddon cooki fortun onegin women night cool follow success lord ring tyler appear varieti role includ film jersey girl lonesom reign stranger incred hulk super space station wildl outsid film play abbott leftov star seri gunpowd hulu seri harlot tyler serv unit nation children fund unicef goodwil ambassador unit state spokesperson givenchi line perfum cosmet daughter steven tyler bebe buell children earli life edit tyler bear rundgren juli mount sinai hospit east harlem york daughter bebe buell model singer playboy playmat miss novemb steven tyler lead singer aerosmith mother name norwegian actress ullmann see ullmann cover march issu guid ancestri includ italian great grandfath german polish english think tyler discov patern great great great great grandfath african american tyler half sibl tyler bear chelsea anna tallarico bear monro tallarico bear matern grandmoth dorothea johnson found protocol school washington buell live rock musician todd rundgren buell unexpect pregnant brief relationship steven tyler give birth juli name daughter rundgren claim todd rundgren biolog father rundgren buell end romant relationship rundgren sign birth certif act father figur includ pay educ steven tyler suspect father ask mother secret reveal truth tyler patern public chang surnam rundgren tyler keep rundgren middl buell state reason claim rundgren father steven tyler heavili addict drug time birth learn truth patern steven develop close relationship work profession appear aerosmith music video crazi aerosmith perform song film armageddon tyler star tyler maintain close relationship rundgren grate love know hold feel like daddi protect strong tyler attend congression school virginia breakwat school waynflet school portland main return york citi mother go york preparatori york citi junior high high school mother research school accommod tyler adhd attend crossroad school art scienc santa monica california graduat york leav continu act career ask youth tyler say childhood teen year work keep troubl everybodi acid parti like crazi work movi tuscani cours differ kind thing regret love life go content career earli work film debut steal beauti mainstream exposur lord ring present offic hit leftov career edit earli work edit tyler receiv model assist paulina porizkova take pictur end interview magazin later star televis commerci bore model career year start decid act take act lesson tyler know televis audienc star alongsid alicia silverston music video aerosmith song crazi film debut steal beauti edit tyler featur film debut silent fall play elder sister autism star comedi drama empir record tyler describ empir record best experi soon land support role jam mangold drama heavi calli naiv young waitress film receiv favor review critic janet maslin note tyler give charm ingenu perform betray self conscious lush good look tyler breakthrough role arthous film steal beauti play luci harmon innoc romant teenag travel tuscani itali intent lose virgin film receiv general mix review tyler perform regard favor critic varieti write tyler perfect accomplic time sweet awkward compos seren actress appear respond effortless intuit camera creat rich sens luci explicit dialogu empir note tyler radiant resembl ganglier young gardner rare opportun enamour break capit composur film direct bernardo bertolucci choos tyler role meet number young girl angel includ tyler music video star alicia silverston bertolucci say miss later say tyler gravita describ york aura promot film tyler say want separ charact product tri damnedest think situat point start rememb star head take nook cranni later appear thing movi fiction wonder rock band call wonder follow whirlwind rise chart quick plung obscur film write direct hank gross million worldwid receiv favor review appear invent abbott daughter patton barbara william charact movi base short stori miller entertain week declar tyler perform love pliant year tyler choos peopl magazin beauti peopl mainstream exposur edit tyler center cast crew premier armageddon kennedi space center florida tyler appear armageddon play daughter bruce willi charact love affleck charact film generat mix review offic success earn million worldwid movi includ song want miss thing kind love aerosmith interview guardian say initi turn role armageddon want turn coupl time biggest reason chang mind scar want reason mean amaz thing career want special movi cast drama onegin film base centuri russian novel alexand pushkin portray tatyana larina star ralph fienn tyler requir master english accent stephen holden york time felt approxim english accent inert film critic financi unsuccess year appear histor comedi film plunkett maclean later appear film direct robert altman cooki fortun women cooki fortun ensembl cast includ glenn close juliann moor chris donnel patricia neal perform receiv critic salon write time tyler act match beauti forlorn altman help snap relax silli snap cartoon sound make take midday swig bourbon lazi genial movi sum emma tyler charact saunter swim cowboy pint wild turkey entertain week write tyler sweet gruff tomboy troublemak women romant comedi tyler play marilyn gynecolog patient richard gere charact lesbian lover daughter play kate hudson lord ring edit tyler play object infatu matt dillon john goodman paul reiser comedi night cool say role definit physic awar peopl awar physic mayb hard anybodi mean love bodi feel comfort skin tough peter traver roll stone write tyler true beauti give role valiant rang limit play amalgam femal perfect tyler premier lord ring return king star featur film lord ring fellowship ring direct peter jackson play maiden arwen miel film base volum tolkien lord ring filmmak approach tyler see perform plunkett maclean learn speak fictiti elvish languag creat tolkien mick sall francisco chronicl note tyler perform love earnest year later tyler star arwen lord ring tower second instal seri film receiv'

    # test_data = pd.Series(np.array(user_input_test.lower()), name='words')
    # # test_data = test_data.str.lower()
    # test_data = test_data.apply(cleanHtml)
    # test_data = test_data.apply(cleanPunc)
    # test_data = test_data.apply(keepAlpha)
    # test_data = test_data.apply(removeStopWords)
    # test_data = test_data.apply(stemming)

    # data = tf_idf(test_data)

    # predictions = perdicet_category(data)

    predictions = pd.read_csv('predictions_example.csv')

    prediction = predictions.loc[0].to_dict()

    return render_template('multilabel_recommendations.html', errors=errors, results=results, predictions=prediction)


# temp
@app.route('/results_lda', methods=['GET','POST'])
def lda():
    return render_template('results_lda.html')



# @app.route('/recommendations', methods=['GET','POST'])
# def recmomendations():
#     return render_template('recommendations.html')


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080, debug=True)
        