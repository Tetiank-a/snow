import bson
from flask_pymongo import PyMongo
from flask import Flask, jsonify, request, Response
from bson import json_util
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import re
import datetime
import User


app = Flask(__name__)
app.secret_key = 'myawesomesecretkey'
app.config["MONGO_URI"] = "mongodb+srv://ronia:2021@cluster0.wdfgt.mongodb.net/snowDB?retryWrites=true&w=majority"
mongodb_client = PyMongo(app)
db = mongodb_client.db


## USERS

@app.route('/users', methods=['POST'])
def create_user():
    # Receiving Data
    new_user = User.User(request)
    response = new_user.add()
    return response


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
    new_user = User.User(request)
    response = new_user.update(_id)
    return response


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


# TASKS
@app.route('/tasks', methods=['POST'])
def create_task():
    # Receiving Data
    name = request.json['name']
    link = request.json['link']
    level_id = request.json['level_id']
    rec_id = request.json['rec_id']
    user_id = request.json['user_id']
    text = request.json['text']

    if link and level_id and rec_id and user_id and text and name:
        id = db.tasks.insert({
            'name': name, 
            'link': link,
            'level_id': level_id,
            'rec_id': rec_id,
            'user_id': user_id,
            'text': text
            })
        response = jsonify({
            '_id': str(id),
            'name': name,
            'link': link,
            'level_id': level_id,
            'rec_id': rec_id,
            'user_id': user_id,
            'text': text
             })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = db.tasks.find()
    response = json_util.dumps(tasks)
    return Response(response, mimetype="application/json")


@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    print(id)
    task = db.tasks.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(task)
    return Response(response, mimetype="application/json")


@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    db.tasks.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Task' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/tasks/<_id>', methods=['PUT'])
def update_task(_id):
    name = request.json['name']
    link = request.json['link']
    level_id = request.json['level_id']
    rec_id = request.json['rec_id']
    user_id = request.json['user_id']
    text = request.json['text']
    if name and link and level_id and rec_id and user_id and text and _id:
        db.tasks.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {
                'name': name, 
                'link': link,
                'level_id': level_id,
                'rec_id': rec_id,
                'user_id': user_id,
                'text': text
                }})
        response = jsonify({'message': 'Task' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
        return not_found()

# RECORDS

@app.route('/records', methods=['POST'])
def create_record():
    # Receiving Data
    xspeed = request.json['xspeed']
    yspeed = request.json['yspeed']
    zspeed = request.json['zspeed']
    angle = request.json['angle']

    if xspeed and yspeed and zspeed and angle:
        id = db.records.insert({
            'xspeed' : [xspeed,],
            'yspeed' : [yspeed,],
            'zspeed' : [zspeed,],
            'angle' : [angle,]
            })
        response = jsonify({
            '_id': str(id),
            'xspeed' : xspeed,
            'yspeed' : yspeed,
            'zspeed' : zspeed,
            'angle' : angle
             })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/records', methods=['GET'])
def get_records():
    records = db.records.find()
    response = json_util.dumps(records)
    return Response(response, mimetype="application/json")


@app.route('/records/<id>', methods=['GET'])
def get_record(id):
    print(id)
    record = db.records.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(record)
    return Response(response, mimetype="application/json")


@app.route('/records/<id>', methods=['DELETE'])
def delete_record(id):
    db.records.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Record' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/records/<_id>', methods=['PUT'])
def update_record(_id):
    xspeed = request.json['xspeed']
    yspeed = request.json['yspeed']
    zspeed = request.json['zspeed']
    angle = request.json['angle']

    if xspeed and yspeed and zspeed and angle:
        db.records.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$push': {
                'xspeed' : xspeed,
                'yspeed' : yspeed,
                'zspeed' : zspeed,
                'angle' : angle
                }})
        response = jsonify({'message': 'Record' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
        return not_found()

# SESSIONS
@app.route('/sessions', methods=['POST'])
def create_session():
    # Receiving Data
    rec_id = request.json['rec_id']
    instructor_id = request.json['instructor_id']
    task_id = request.json['task_id']
    user_id = request.json['user_id']
    dtstart = datetime.datetime.strptime(request.json['dtstart'], '%Y-%m-%d %H:%M:%S.%f')
    dtfinish = datetime.datetime.strptime(request.json['dtfinish'], '%Y-%m-%d %H:%M:%S.%f')

    if rec_id and instructor_id and task_id and user_id and dtstart and dtfinish:
        id = db.sessions.insert({
            'rec_id': rec_id, 
            'instructor_id': instructor_id,
            'task_id': task_id,
            'user_id': user_id,
            'dtstart': dtstart,
            'dtfinish': dtfinish
            })
        response = jsonify({
            '_id': str(id),
            'rec_id': rec_id, 
            'instructor_id': instructor_id,
            'task_id': task_id,
            'user_id': user_id,
            'dtstart': dtstart,
            'dtfinish': dtfinish
             })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/sessions', methods=['GET'])
def get_sessions():
    sessions = db.sessions.find()
    response = json_util.dumps(sessions)
    return Response(response, mimetype="application/json")


@app.route('/sessions/<id>', methods=['GET'])
def get_session(id):
    print(id)
    session = db.sessions.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(session)
    return Response(response, mimetype="application/json")


@app.route('/sessions/<id>', methods=['DELETE'])
def delete_session(id):
    db.sessions.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Session' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/sessions/<_id>', methods=['PUT'])
def update_session(_id):
    rec_id = request.json['rec_id']
    instructor_id = request.json['instructor_id']
    task_id = request.json['task_id']
    user_id = request.json['user_id']
    dtstart = datetime.datetime.strptime(request.json['dtstart'], '%Y-%m-%d %H:%M:%S.%f')
    dtfinish = datetime.datetime.strptime(request.json['dtfinish'], '%Y-%m-%d %H:%M:%S.%f')
    if rec_id and instructor_id and task_id and user_id and dtstart and dtfinish:
        db.sessions.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {
                'rec_id': rec_id, 
                'instructor_id': instructor_id,
                'task_id': task_id,
                'user_id': user_id,
                'dtstart': dtstart,
                'dtfinish': dtfinish
                }})
        response = jsonify({'message': 'Session' + _id + 'Updated Successfuly'})
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
