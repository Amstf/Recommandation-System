import pandas as pd
import numpy as np
import turicreate
import os
from flask import Flask , redirect,url_for,request,render_template,jsonify
from flask_cors import CORS
import json
import pymongo

app = Flask(__name__)


client=pymongo.MongoClient("mongodb://localhost/buyify")

db = client['buyify']
collection = db['ratings']
@app.route("/ReadCSV/<user_id>")
def ReadCSV(user_id):
    documents = collection.find()
    response = []
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
    
    df = pd.DataFrame(response)
    ratings_train=df[['user','product','rating']]
    train_data = turicreate.SFrame(ratings_train)
    item_sim_model = turicreate.item_similarity_recommender.create(train_data, user_id='user', item_id='product', target='rating', similarity_type='cosine')
    #Making recommendations
    item_sim_recomm = item_sim_model.recommend(users=[user_id],k=10)
    recommendation=[]
    for i in item_sim_recomm :
        recommendation.append(i['product'])
    response = jsonify(message=recommendation)

    # Enable Access-Control-Allow-Origin
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
    # return render_template('index.html',result=recommendation)

if __name__ == '__main__':
    app.run(debug=True,port=7000)

