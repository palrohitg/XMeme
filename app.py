import pymongo
from pymongo import MongoClient
import urllib.parse
from flask import Flask, render_template, request, jsonify, Response
import json
import os
import ast
from flask_cors import CORS, cross_origin

app = Flask(__name__)

# Credentials of Database
username = urllib.parse.quote_plus('root')
password = urllib.parse.quote_plus("root1234")

url = "mongodb+srv://{}:{}@cluster0.o2yph.mongodb.net/XMEME?retryWrites=true&w=majority".format(
    username, password)

cluster = MongoClient(url)
db = cluster['XMEME']
meme = db['meme']


# Get all the meme details
@app.route("/")
@cross_origin()
def home():
    documents = meme.find({})
    response = [{item: data[item] for item in data if item != '_id'}
                for data in documents]
    return render_template("index.html", result_list=response)


# Post API
@app.route("/memes", methods=['GET', 'POST'])
@cross_origin()
def create_meme():
    if request.method == "POST":
        content = request.get_json(force=True)
        meme_url = content['meme_url']
        meme_owner = content['meme_owner']
        meme_caption = content['meme_caption']

        # Insert into database
        meme.insert_one({"id ": meme.find().count()+1, "meme_owner": meme_owner,
                         "meme_caption": meme_caption, "meme_url": meme_url})

        resp = jsonify('User added successfully!')
        resp.status_code = 200
        return resp

    documents = meme.find({})
    response = [{item: data[item] for item in data if item != '_id'}
                for data in documents]
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


@app.route("/memes/<id>", methods=["GET"])
def get_meme_by_id(id):
    documents = meme.find({"id": id})
    print(documents)
    for data in documents:
        print(data)
    response = [{item: data[item] for item in data if item != '_id'}
                for data in documents]
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
