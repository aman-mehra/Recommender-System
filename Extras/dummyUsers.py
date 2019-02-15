import pandas as pd
from pymongo import MongoClient
import math
import random

K = 12
N = 300

#client = MongoClient('mongodb://localhost:27017')
client = MongoClient("mongodb://guest:guest@cluster1-shard-00-00-85a72.mongodb.net:27017,cluster1-shard-00-01-85a72.mongodb.net:27017,cluster1-shard-00-02-85a72.mongodb.net:27017/test?ssl=true&replicaSet=cluster1-shard-0&authSource=admin&retryWrites=true")

db = client['MovieRecommenderDb']
u_col = db["UserCol"]
m_col = db["MovieCol"]

movieIdsList = []

cursor = m_col.find({})
for document in cursor:
      movieIdsList.append(document["_id"])


user_headers = ["userId","movieId","rating"]
user_ratings = pd.read_csv("ml-latest-small/ratings.csv",usecols=user_headers)

customUid = 1
prevId = 1
nextId = 1

wait_for_next_user = False

uRats = []

for _, r in user_ratings.iterrows():
    nextId = r[0]
    movId = int(r[1])
    movRating = int(math.ceil(r[2]))
    
    if nextId != prevId:
        if len(uRats)>=K:
            random.shuffle(uRats)
            record = {"_id":customUid,"ratings":uRats[:K]}
            u_col.insert(record)
            customUid += 1
        uRats = []
        wait_for_next_user = False
        
        if(customUid%20==0):
            print customUid
            
        if customUid>N:
            break

    if not wait_for_next_user:
        if movId in movieIdsList:
            uRats.append([movId,movRating])
        elif movId > movieIdsList[-1]:
            wait_for_next_user =True
            
    prevId = nextId

        
    
