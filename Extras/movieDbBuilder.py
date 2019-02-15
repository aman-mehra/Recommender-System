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

#client = MongoClient('mongodb://localhost:27017')
#client = MongoClient("mongodb+srv://guest:guest@cluster1-85a72.mongodb.net/test?retryWrites=true")
client = MongoClient("mongodb://guest:guest@cluster1-shard-00-00-85a72.mongodb.net:27017,cluster1-shard-00-01-85a72.mongodb.net:27017,cluster1-shard-00-02-85a72.mongodb.net:27017/test?ssl=true&replicaSet=cluster1-shard-0&authSource=admin&retryWrites=true")

db = client['MovieRecommenderDb']
collection = db["MovieCol"]

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
    movieId = mov[0]
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
        
        for _, row in movie_links.iterrows():
            if row[0]==movieId :
                imdbURI = str(row[1])
                imdbURI = "0"*(7-len(imdbURI))+imdbURI
                url = imdbBase+imdbURI
                response = urllib2.urlopen(url)
                html = response.read()
                soup = BeautifulSoup(html,"html5lib")
                imgdiv = soup.find('div', {'class': 'poster'})
                div_children  = imgdiv.findChildren("img" , recursive=True)
                img_src = ""
                for child in div_children:
                   img_src = child["src"]
                record = {"_id":movieId,"Name":name,"Year":year,"Imdb_url":url,"Img_src":img_src}
                collection.insert(record)
                break
        if(movieId%20==0):
            print total_records()
    if(len(below_thresh)==0 and len(classes.keys())==19):
        break
    
print classes
print total_records()
            

##for index, row in movie_links.iterrows():
##    movieUrlId = str(row[1])
##    movieUrlId = "0"*(7-len(movieUrlId))+movieUrlId
##    url = imdbBase+movieUrlId
##    response = urllib2.urlopen(url)
##    html = response.read()
##    soup = BeautifulSoup(html,"html5lib")
##    imgdiv = soup.find('div', {'class': 'poster'})
##    div_children  = imgdiv.findChildren("img" , recursive=True)
##    for child in div_children:
##       print child["src"]
##       img_data = requests.get(child["src"]).content
##    with open('image_name.jpg', 'wb') as handler:
##        handler.write(img_data)        
##    break
   

