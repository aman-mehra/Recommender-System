
# Recommender-System
An application which recommends movies to a user after he/she rates some movies. This uses user-user and item-item based collaborative filtering along with a matrix factorization approach based on the FunkSVD algorithm

### Dependancies

The followng packages will need to be installed. Requirements.txt exhaustively lists all the requirements as well.

* pandas
* numpy
* pymongo
* requests
* scikit-learn
* flask
* flask-cors

### CodeBase and Directory Structure

The codebase consists of python code which is used to create and access the database of movies and users as well as develop the recommendation algorithms and run the server.The webpage to interact with the application is present in the index.html file.

The directory Extras contains the MongoDb database used by the application along with a dataset of movies and ratings taken from the grouplens research group online. The python files present were used to scrape data from the web and build the collections in the MongoDb database. 

The MongoDb Database consists of two collections one which contains the movie names, year of release and urls of their thumbnail images
while the second collection contains ratings of dummy users

Below is a brief explanation of what each file does:
* [backend.py](backend.py) : This runs the flask server which handles the GET and POST requests.It manages interractions between MongoConnector and Recommender.
* [MongoConnector.py](MongoConnector.py) : This file handles all the interactions with the MongoDb database.It contains routines to fetch data in all the various forms required by the appliation.
* [Recommender.py](Recommender.py) : This contains implementations for all the recommendation algorithms, namely User-User collaborative filtering, Item-Item collaborative filtering and the Matrix Factorization based approach wherin it uses the FunkSVD algorithm.
* [dbanalyzer.py](Extras/dbanalyzer.py) : This is a utility to validate the distribuion of various genres in the movies stored in the database
* [dummyUsers.py](Extras/dummyUsers.py) : This is a utility to build the database containing dummy users and their ratings
* [movieDbBuilder.py](Extras/movieDbBuilder.py) : This is a utility to build the database containing the movies and their additional information
* [index.html](index.html) : This is the webpage to interact with the application

## Implementation Notes

* Have used Pearson correlation for the user-user collaborative filtering
* Used cosine similarity for item-item cosine collaborative filtering
* The matrix factorization approach pre-trains and stores weights and features of original database(in [chkpt_P](chkpt_P.csv) and [chkpt_Q](chkpt_Q.csv)) and then partially retrains as it gets requests form users online. For this purpose most methods in its implementation have two modes of running - offline and online
* The number of user ratings accepted are 12 

## Running the application

Click [here](https://amehra-github.github.io/Recommender-System/index.html) to see it in action.

### Deployment details

* The python server has been deployed on heroku. 
* The MongoDb database is stored on the cloud using mLab(recently acquired by MongoDb and renamed MongoDb Atlas)
* The website is hosted using gh-pages pages on github

### References

* FunkSVD and Matrix Factorization - Referred to [Medium](https://medium.com/datadriveninvestor/how-funk-singular-value-decomposition-algorithm-work-in-recommendation-engines-36f2fbf62cac) and [Coursera](https://www.coursera.org/learn/matrix-factorization)
* Dataset - [MovieLens](https://grouplens.org/datasets/movielens/)
* Collaborative Filtering Algorithms - [here](https://hackernoon.com/introduction-to-recommender-system-part-1-collaborative-filtering-singular-value-decomposition-44c9659c5e75)



