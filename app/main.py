from flask_pymongo import PyMongo
from flask import Flask, jsonify, request, Response
from bson import json_util
from bson.objectid import ObjectId
from DB.UsersT import do
from werkzeug.wrappers import response
from classes import User, Level, Record, Advice, Session, Task
import os
from dotenv import load_dotenv


app = Flask(__name__)
app.secret_key = 'myawesomesecretkey'
load_dotenv()
app.config["MONGO_URI"] = f'mongodb+srv://ronia:{os.environ.get("password")}'\
    '@cluster0.wdfgt.mongodb.net/snowDB?'\
    'retryWrites=true&w=majority'
mongodb_client = PyMongo(app)
db = mongodb_client.db


# USERS

@app.route('/api/signup', methods=['POST'])
def signup():
    # Receiving Data
    if (('password' in request.json) and
        ('password_repeat' in request.json) and
            (request.json['password'] == request.json['password_repeat'])):
        new_user = User.User(request)
        response = new_user.add()
    else:
        response = response = jsonify({'message': 'Passwords do not match'})
        response.status_code = 400
    return response


@app.route('/api/users', methods=['POST'])
def create_user():
    # Receiving Data
    new_user = User.User(request)
    response = new_user.add()
    return response


@app.route('/api/users', methods=['GET'])
def get_users():
    users = db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype="application/json")


@app.route('/api/users/<id>', methods=['GET'])
def get_user(id):
    print(id)
    user = db.users.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")


@app.route('/api/users/<id>', methods=['DELETE'])
def delete_user(id):
    db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/api/users/<_id>', methods=['PUT'])
def update_user(_id):
    new_user = User.User(request)
    response = new_user.update(_id)
    return response


# LEVELS
@app.route('/api/levels', methods=['POST'])
def create_level():
    # Receiving Data
    new_level = Level.Level(request)
    response = new_level.add()
    return response


@app.route('/api/levels', methods=['GET'])
def get_levels():
    levels = db.levels.find()
    response = json_util.dumps(levels)
    return Response(response, mimetype="application/json")


@app.route('/api/levels/<id>', methods=['GET'])
def get_level(id):
    print(id)
    level = db.levels.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(level)
    return Response(response, mimetype="application/json")


@app.route('/api/levels/<id>', methods=['DELETE'])
def delete_level(id):
    db.levels.delete_one({'_id': ObjectId(id)})
    # TODO: do not delete if this level is used
    response = jsonify({'message': 'Level' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/api/levels/<_id>', methods=['PUT'])
def update_level(_id):
    new_level = Level.Level(request)
    new_level.update(_id)
    return response


# TASKS
@app.route('/api/tasks', methods=['POST'])
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


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = db.tasks.find()
    response = json_util.dumps(tasks)
    return Response(response, mimetype="application/json")


@app.route('/api/tasks/<id>', methods=['GET'])
def get_task(id):
    print(id)
    task = db.tasks.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(task)
    return Response(response, mimetype="application/json")


@app.route('/api/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    db.tasks.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Task' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/api/tasks/<_id>', methods=['PUT'])
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


@app.route('/api/records', methods=['POST'])
def create_record():
    # Receiving Data
    new_record = Record.Record(request)
    response = new_record.add()
    return response


@app.route('/api/records', methods=['GET'])
def get_records():
    records = db.records.find()
    response = json_util.dumps(records)
    return Response(response, mimetype="application/json")


@app.route('/api/records/<id>', methods=['GET'])
def get_record(id):
    print(id)
    record = db.records.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(record)
    return Response(response, mimetype="application/json")


@app.route('/api/records/<id>', methods=['DELETE'])
def delete_record(id):
    db.records.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Record' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/api/records/<_id>', methods=['PUT'])
def update_record(_id):
    new_record = Record.Record(request)
    response = new_record.update(_id)
    return response


# SESSIONS
@app.route('/api/sessions', methods=['POST'])
def create_session():
    # Receiving Data
    rec_id = request.json['rec_id']
    instructor_id = request.json['instructor_id']
    task_id = request.json['task_id']
    user_id = request.json['user_id']
    dtstart = request.json['dtstart']
    dtfinish = request.json['dtfinish']

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


@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    sessions = db.sessions.find()
    response = json_util.dumps(sessions)
    return Response(response, mimetype="application/json")


@app.route('/api/sessions/<id>', methods=['GET'])
def get_session(id):
    print(id)
    session = db.sessions.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(session)
    return Response(response, mimetype="application/json")


@app.route('/api/sessions/<id>', methods=['DELETE'])
def delete_session(id):
    db.sessions.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Session' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/api/sessions/<_id>', methods=['PUT'])
def update_session(_id):
    rec_id = request.json['rec_id']
    instructor_id = request.json['instructor_id']
    task_id = request.json['task_id']
    user_id = request.json['user_id']
    dtstart = request.json['dtstart']
    dtfinish = request.json['dtfinish']

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
        response = jsonify(
            {'message': 'Session' + _id + 'Updated Successfuly'})
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

## ADVICE (ML)


@app.route('/api/advice', methods=['POST'])  # TODO: take id
def recieve_advice():
    new_advice = Advice.Advice(request)
    response = new_advice.get_advice()
    #response = json_util.dumps(result_data)
    return response


# BACK UP

@app.route('/api/backup', methods=['GET'])
def save_all():

    # Sessions
    a1 = db.sessions.find()
    res = json_util.dumps(a1, indent=2)
    with open('json/sessions.json', 'w') as file:
        file.write(res)

    # Levels
    a1 = db.levels.find()
    res = json_util.dumps(a1, indent=2)
    with open('json/levels.json', 'w') as file:
        file.write(res)

    # Records
    a1 = db.records.find()
    res = json_util.dumps(a1, indent=2)
    with open('json/records.json', 'w') as file:
        file.write(res)

    # Tasks
    a1 = db.tasks.find()
    res = json_util.dumps(a1, indent=2)
    with open('json/tasks.json', 'w') as file:
        file.write(res)

    # Users
    a1 = db.users.find()
    res = json_util.dumps(a1, indent=2)
    with open('json/users.json', 'w') as file:
        file.write(res)

    # Advice
    a1 = db.advice.find()
    res = json_util.dumps(a1, indent=2)
    with open('json/advice.json', 'w') as file:
        file.write(res)

    response = jsonify({'message': 'Backup completed Successfuly'})
    response.status_code = 200
    return response


@app.route('/api/create', methods=['GET'])  # TODO: take id
def create_table():
    # do()
    response = jsonify({'message': 'DB created'})
    response.status_code = 200
    return response

# A welcome message to test our server


@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
