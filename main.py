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

@app.route("/")
def hello():
    return "Hello World!"

# USERS
@app.route('/users', methods=['POST'])
def create_user():
    # Receiving Data
    username = request.json['username']
    email = request.json['email']
    level_id = request.json['level_id']
    password = request.json['password']

    if username and email and level_id and password:
        hashed_password = generate_password_hash(password)
        id = db.users.insert(
            {'username': username, 'email': email, 'level_id': level_id, 'password': hashed_password})
        response = jsonify({
            '_id': str(id),
            'username': username,
            'password': password,
            'email': email,
            'level_id': level_id
        })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/users', methods=['GET'])
def get_users():
    users = db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype="application/json")


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    print(id)
    user = db.users.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/users/<_id>', methods=['PUT'])
def update_user(_id):
    username = request.json['username']
    email = request.json['email']
    level_id = request.json['level_id']
    password = request.json['password']
    if username and email and password and _id:
        hashed_password = generate_password_hash(password)
        db.users.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'username': username, 'email': email, 'level_id': level_id, 'password': hashed_password}})
        response = jsonify({'message': 'User' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
      return not_found()

# LEVELS
@app.route('/levels', methods=['POST'])
def create_level():
    # Receiving Data
    name = request.json['name']

    if name:
        id = db.levels.insert(
            {'name': name})
        response = jsonify({
            '_id': str(id),
            'name': name
        })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/levels', methods=['GET'])
def get_levels():
    levels = db.levels.find()
    response = json_util.dumps(levels)
    return Response(response, mimetype="application/json")


@app.route('/levels/<id>', methods=['GET'])
def get_level(id):
    print(id)
    level = db.levels.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(level)
    return Response(response, mimetype="application/json")


@app.route('/levels/<id>', methods=['DELETE'])
def delete_level(id):
    db.levels.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Level' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/levels/<_id>', methods=['PUT'])
def update_level(_id):
    name = request.json['name']
    if name and _id:
        db.levels.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'name': name}})
        response = jsonify({'message': 'Level' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
      return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response