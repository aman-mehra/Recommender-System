import numpy as np
from pymongo import MongoClient
import pandas as pd

class MongoCon:

    def __init__(self,K=12):
        #self.client = MongoClient("localhost", 27017)
        self.client = MongoClient("mongodb://guest:guest@cluster1-shard-00-00-85a72.mongodb.net:27017,cluster1-shard-00-01-85a72.mongodb.net:27017,cluster1-shard-00-02-85a72.mongodb.net:27017/test?ssl=true&replicaSet=cluster1-shard-0&authSource=admin&retryWrites=true")
        self.db = self.client['MovieRecommenderDb']
        self.u_collection = self.db["UserCol"]
        self.m_collection = self.db["MovieCol"]
        self.id_to_idx = {}
        self.idx_to_id = {}
        self.K = K
        self.movies = 0

    def translate_idx_to_id(self,inds):
        ids = []
        for i in inds:
            ids.append(self.idx_to_id[i])
        return ids

    def transalate_id_to_idx(self,ids):
        inds = []
        for i in ids:
            inds.append(self.id_to_idx[i])
        return inds

    def get_k_random(self):
        inds = list(self.id_to_idx.values())
        np.random.shuffle(inds)
        return inds[:self.K]

    def fetch_records(self,idx):
        ids = self.translate_idx_to_id(idx)
        mov_cursor = self.m_collection.find({})
        df_recs = pd.DataFrame(list(mov_cursor))
        records ={}
        for idx,row in df_recs.iterrows():
            if int(row["_id"]) in ids:
                records[int(row["_id"])]=[row["Name"],row["Year"],row["Img_src"]]
        return records

    def build_user(self,ids,ratings):
        inds = self.transalate_id_to_idx(ids)
        user = np.zeros((self.movies,1))
        for i in range(len(inds)):
            user[inds[i],0]=ratings[i]
        return user

    def build_matrix(self):
        cursor_m = self.m_collection.find({},{ "_id": 1})
        cursor_u = self.u_collection.find({},{ "_id": 0})
        
        df_m =  pd.DataFrame(list(cursor_m))
        df_u =  pd.DataFrame(list(cursor_u))
        
        for idx,row in df_m.iterrows():
            self.id_to_idx[row[0]] = idx
            self.idx_to_id[idx] = row[0]

        n_movies = df_m.shape[0]
        n_users = df_u.shape[0]

        self.movies =n_movies

        arr = np.zeros((n_movies,n_users))        
        
        for idx,row in df_u.iterrows():
            for mov_rating in row[0]:
                arr[self.id_to_idx[mov_rating[0]],idx] = mov_rating[1]

        return arr
