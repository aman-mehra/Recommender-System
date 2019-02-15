import pandas as pd
import urllib2
from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient

def enter_record(genres):
    allow_low = False
    for i in genres:
        if not classes.has_key(i):
            allow_low = True
        else:
            if i in below_thresh:
                allow_low = True
            elif classes[i]>=max_thresh:
                return False
    return allow_low

def update_threshes(genres):
    for i in genres:
        if i in below_thresh:
            if classes[i]>=thresh:
                below_thresh.remove(i)
                above_thresh.append(i)

def total_records():
    s=0
    for k in classes.keys():
        s+=classes[k]
    return s

#imdbId must be padded with 0s on left to extend length to 7
movie_link_col_headers = ["movieId","imdbId"]
movie_links = pd.read_csv("ml-latest-small/links.csv",usecols=movie_link_col_headers)

movie_name_col_headers = ["movieId","title","genres"]
movie_names = pd.read_csv("ml-latest-small/movies.csv",usecols=movie_name_col_headers)

imdbBase = "https://www.imdb.com/title/tt"

classes = {}
below_thresh = []
above_thresh = []
thresh = 15
max_thresh = 35

for _, mov in movie_names.iterrows():
    name = mov[1][:-6]
    year = mov[1][-5:-1]
    genres = mov[2].split("|")
    allow = enter_record(genres)
    if allow:
        for i in genres:
            try:
                classes[i]+=1
            except Exception:
                classes[i]=1
                below_thresh.append(i)
        update_threshes(genres)
            
    movieId = mov[0]
    
    if(len(below_thresh)==0 and len(classes.keys())==19):
        break
print classes
print total_records()
            
   

