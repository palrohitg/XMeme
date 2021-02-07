import pymongo
from pymongo import MongoClient
import urllib.parse
from flask import Flask, render_template, request, jsonify, Response
import json
import os
import ast

app = Flask(__name__)

username = urllib.parse.quote_plus('root')
password = urllib.parse.quote_plus("root1234")

url = "mongodb+srv://{}:{}@cluster0.o2yph.mongodb.net/XMEME?retryWrites=true&w=majority".format(
    username, password)

cluster = MongoClient(url)
db = cluster['XMEME']
meme = db['meme']


# Get all the meme details
@app.route("/")
def home():
    documents = meme.find({})
    response = [{item: data[item] for item in data if item != '_id'}
                for data in documents]
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


# Post API
@app.route("/memes", methods=['POST'])
def create_meme():
    data = request.json
    if data is None or data == {} or 'Document' not in data:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')

    response = meme.insert_one(data['Document'])
    output = {'Status': 'Successfully Inserted',
              'Document_ID': str(response.inserted_id)}
    response = output
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=True)
