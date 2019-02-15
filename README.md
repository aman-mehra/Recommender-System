## Recommender-System
<br/>
# CodeBase and Directory Structure
The codebase consists of python code used to create and access the database of movies
and users as well as develop the recommendation algorithms and run the server. 
The webpage to interact with the application is present in the index.html file
The following list presents the use of each file:
- [backend.py](backend.py) : This runs the flask server which handles the GET and POST requests. 
	It manages interractions between MongoConnector and Recommender.
- [MongoConnector.py](MongoConnector.py) : This file handles all the interractions with the MongoDb database.
	It contains routines to fetch data in all the various forms required by the appliation.
- [Recommender.py](Recommender.py) : This contains implementations for all the recommendation 
	algotithms, namely User-User collaborative filtering, Item-Item collaborative filtering 
	and the Matrix Factorization based approach wherin it uses the FunkSVD algorithm.

https://amehra-github.github.io/Recommender-System/index.html