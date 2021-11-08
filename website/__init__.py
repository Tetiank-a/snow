from flask_pymongo import PyMongo
from flask import Flask, jsonify, request, Response
from bson import json_util
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'myawesomesecretkey'
app.config["MONGO_URI"] = "mongodb+srv://ronia:2021@cluster0.wdfgt.mongodb.net/snowDB?retryWrites=true&w=majority"
mongodb_client = PyMongo(app)
db = mongodb_client.db