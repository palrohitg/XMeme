import pymongo
from pymongo import MongoClient
import urllib.parse
from flask import Flask, render_template, request, jsonify, Response, redirect, url_for
import json
import os
import ast
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo

app = Flask(__name__)

# Local Data-Base Connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/XMEME"

# Cloud Data-Base Connection
# username = urllib.parse.quote_plus('root')
# password = urllib.parse.quote_plus("root1234")
# url = "mongodb+srv://{}:{}@cluster0.o2yph.mongodb.net/XMEME?retryWrites=true&w=majority".format(
#     username, password)
# app.config["MONGO_URI"] = url

mongo = PyMongo(app)


@app.route("/", methods=["GET", "POST"])
@cross_origin()
def home():

    if request.method == "POST":
        name = request.form['memeOwner']
        caption = request.form['memeCaption']
        url = request.form['memeURL']
        mongo.db.meme.insert_one({"id": mongo.db.meme.find().count()+1, "name": name,
                                  "caption": caption, "url": url})
        return redirect(url_for("home"))
    else:
        documents = mongo.db.meme.find({})
        response = [{item: data[item] for item in data if item != '_id'}
                    for data in documents]
        sorted_response = sorted(response, key=lambda i: i['id'], reverse=True)
        print(sorted_response)
        return render_template("index.html", result_list=sorted_response)


# Get all memes(Endpoint) + create new memes(End`point)
@app.route("/memes", methods=['GET', 'POST'])
@cross_origin()
def create_meme():
    if request.method == "POST":
        content = request.get_json(force=True)
        name = content['name']
        caption = content['caption']
        url = content['url']

        # Duplicate post exists in the database
        name_res = mongo.db.meme.count_documents({"name": name})
        caption_res = mongo.db.meme.count_documents({"caption": caption})
        url_res = mongo.db.meme.count_documents({"url": url})
        if(name_res != 0 and caption_res != 0 and url_res != 0):
            return " dupilcate 409"
        else:
            # Instering meme into db query
            mongo.db.meme.insert_one({"id": mongo.db.meme.find().count()+1, "name": name,
                                      "caption": caption, "url": url})
            id = mongo.db.meme.find().count()
            return {'id': str(id)}, 200

    documents = mongo.db.meme.find({})
    response = [{item: data[item] for item in data if item != '_id'}
                for data in documents]
    return Response(response=json.dumps(response, indent=3),
                    status=200,
                    mimetype='application/json')


# Update meme by id(Endpoint) + get meme by id(Endpoint)
@ app.route("/memes/<int:id>", methods=["GET", "PATCH"])
@ cross_origin()
def get_meme_by_id(id):

    if request.method == "PATCH":
        content = request.get_json(force=True)
        url = content['url']
        caption = content['caption']
        query = {"id": id}
        new_query = {
            "$set": {"caption": caption, "url": url}}
        mongo.db.meme.update_one(query, new_query)
        return "200"

    else:
        try:
            data = mongo.db.meme.find_one({"id": id})
            response = [{item: data[item] for item in data if item != '_id'}]
            return Response(response=json.dumps(response, indent=3),
                            status=200,
                            mimetype='application/json')
        except:
            return "404"


@ app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(port=8081, debug=True)
