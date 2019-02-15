#import urllib2
from flask import Flask
from flask import request
from flask import jsonify
import requests
from flask_cors import CORS,cross_origin

from MongoConnector import *
from Recommender import *

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

## Initializations
dbcon  = MongoCon()
#print 1
mat = dbcon.build_matrix()
#print 2
collabFilt = CollaborativeFiltRecs()
factRec = MatFactRecs(mat)
factRec.train()

@app.route('/')
@cross_origin()
def check():
    return '<h1>RUNNING!!!!</h1>'

@app.route('/getmovies',methods = ['GET'])
@cross_origin()
def render_info():
    inds = dbcon.get_k_random()
    #print inds
    movies = dbcon.fetch_records(inds)
    return jsonify(movies)

@app.route('/postratings',methods = ['POST'])
@cross_origin()
def new_user_ratings():
    data = request.get_json()
    ids = []
    ratings =[]
    for k,v in data.items():
        ids.append(int(k))
        ratings.append(float(v))
    #print ids
    #print ratings
    user = dbcon.build_user(ids,ratings)
    recs_u  = dbcon.fetch_records(collabFilt.user_user_filter(user,mat))
    recs_i = dbcon.fetch_records(collabFilt.item_item_filter(user,mat))
    recs_mf = dbcon.fetch_records(factRec.get_user_pred(user))
    recommendations = {"U":recs_u,"I":recs_i,"M":recs_mf}
    return jsonify(recommendations)

if __name__=='__main__':
    #app.debug=True
    app.run(host="0.0.0.0",port=5000)

"""
http://127.0.0.1:5000/postratings
{
	"123":"1",
	"231":"5"
}

"""

