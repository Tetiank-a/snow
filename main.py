from flask_pymongo import PyMongo
from flask import Flask

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://ronia:2021@cluster0.wdfgt.mongodb.net/test?retryWrites=true&w=majority"
mongodb_client = PyMongo(app)
db = mongodb_client.db

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/add_one")
def add_one():
    db.todos.insert_one({'name': "Ronia", 'book': "Narnia"})
    return "done 1."

@app.route("/add_many")
def add_many():
    db.todos.insert_many([
        {'name': "Ronia_clone", 'book': "Shadow and Bone"},
        {'name': "Tania", 'book': "book2"},
        {'name': "Misha", 'book': "book3"},
        {'name': "Nastya", 'book': "book4"},
        ])
    return "done many."