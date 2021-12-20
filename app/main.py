from datetime import datetime
from flask_pymongo import PyMongo
from flask import Flask, jsonify, request, Response
from bson import json_util
from bson.objectid import ObjectId
from werkzeug.security import check_password_hash, generate_password_hash
from DB.UsersT import do
from werkzeug.wrappers import response
from classes import User, Level, Record, Advice, Session, Task, Location
import os
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
# import dateutil.parser

date_format = "%Y-%m-%dT%H:%M:%S.%fZ"



app = Flask(__name__)
CORS(app)
app.secret_key = 'myawesomesecretkey'
load_dotenv()
app.config["MONGO_URI"] = f'mongodb+srv://ronia:{os.environ.get("password")}'\
    '@cluster0.wdfgt.mongodb.net/snowDB?'\
    'retryWrites=true&w=majority'
mongodb_client = PyMongo(app)
db = mongodb_client.db

app.config["JWT_SECRET_KEY"] = "ronald"
jwt = JWTManager(app)

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
        response = jsonify({'message': 'Passwords do not match'})
        response.status_code = 400
    return response


@app.route('/api/login', methods=['POST'])
def login():
    # Receiving Data
    if (('password' in request.json) and
            ('email' in request.json)):
        # hashed_password = generate_password_hash(request.json['password'])
        new_user = db.users.find_one({"email": request.json['email']})
        level_admin = str(db.levels.find_one({"name": "admin"})['_id'])
        level_instructor = str(db.levels.find_one({"name": "instructor"})['_id'])
        print(new_user['password'])
        print(generate_password_hash(request.json['password']))
        print(request.json['password'])

       # print(check_password_hash("pbkdf2:sha256:260000$ZCfafTi6ivBJcM7Y$eb7955455f88c8e86000abcb3d195f059b2a6befe3715b0b23b7eb9c918f1a12", str("qwerty123")))
        if (new_user != None and check_password_hash(new_user['password'], request.json['password'])):
            role = 'user'
            if new_user['level_id'] == level_admin:
                role = 'admin'
            else:
                if new_user['level_id'] == level_instructor:
                    role = 'instructor'
            access_token = create_access_token(identity=str(new_user['_id']))
            response = jsonify(
                {'token': access_token, '_id': str(new_user['_id']), 'role': role})
            response.status_code = 200
        else:
            response = jsonify({'message': str("no such user")})
            response.status_code = 400
    else:
        response = jsonify({'message': 'Email or password field is empty'})
        response.status_code = 400
    return response


@app.route('/api/users', methods=['POST'])
def create_user():
    # Receiving Data
    new_user = User.User(request)
    response = new_user.add()
    return response


@app.route('/api/users', methods=['GET'])
@jwt_required()
def get_users():
    users = db.users.find()
    response = json_util.dumps(users)
    json_dict = json_util.loads(response)
    i = 0

    for x in json_dict:
        level = db.levels.find_one({'_id': ObjectId(x['level_id']), })
        json_dict[i]['level'] = {'_id': str(
            level['_id']), 'name': level['name']}
        json_dict[i]['_id'] = str(json_dict[i]['_id'])
        if 'level_id' in json_dict[i]:
            del json_dict[i]['level_id']
        if 'password' in json_dict[i]:
            del json_dict[i]['password']
        i = i + 1
    response = json_util.dumps(json_dict)
    return Response(response, mimetype="application/json")


@app.route('/api/users/<id>', methods=['GET'])
@jwt_required()
def get_user(id):

    users = db.users.find({'_id': ObjectId(id), })
    response = json_util.dumps(users)
    json_dict = json_util.loads(response)
    i = 0

    for x in json_dict:
        level = db.levels.find_one({'_id': ObjectId(x['level_id']), })
        json_dict[i]['level'] = {'_id': str(
            level['_id']), 'name': level['name']}
        json_dict[i]['_id'] = str(json_dict[i]['_id'])
        if 'level_id' in json_dict[i]:
            del json_dict[i]['level_id']
        if 'password' in json_dict[i]:
            del json_dict[i]['password']
        i = i + 1
    response = json_util.dumps(json_dict)
    return Response(response, mimetype="application/json")


@app.route('/api/users/<id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/api/users/<_id>', methods=['PUT'])
@jwt_required()
def update_user(_id):
    username = request.json['username']
    email = request.json['email']
    level_id = request.json['level']['_id']
    password = str(db.users.find_one({'_id': ObjectId(_id), })['password'])
    db.users.update_one(
        {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {
            'username': username,
            'email': email,
            'level_id': level_id,
            'password': password
        }
        })
    response = jsonify(
        {'message': 'User ' + _id + ' Updated Successfuly'})
    response.status_code = 200
    return response


# LEVELS
@app.route('/api/levels', methods=['POST'])
@jwt_required()
def create_level():
    # Receiving Data
    new_level = Level.Level(request)
    response = new_level.add()
    return response


@app.route('/api/levels', methods=['GET'])
@jwt_required()
def get_levels():
    levels = db.levels.find()
    response = json_util.dumps(levels)
    json_dict = json_util.loads(response)
    i = 0
    for x in json_dict:
        json_dict[i]['_id'] = str(json_dict[i]['_id'])
        i = i + 1
    response = json_util.dumps(json_dict)
    return Response(response, mimetype="application/json")


@app.route('/api/levels/<id>', methods=['GET'])
@jwt_required()
def get_level(id):
    print(id)
    level = db.levels.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(level)
    return Response(response, mimetype="application/json")


@app.route('/api/levels/<id>', methods=['DELETE'])
@jwt_required()
def delete_level(id):
    db.levels.delete_one({'_id': ObjectId(id)})
    # TODO: do not delete if this level is used
    response = jsonify({'message': 'Level' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/api/levels/<_id>', methods=['PUT'])
@jwt_required()
def update_level(_id):
    new_level = Level.Level(request)
    new_level.update(_id)
    return response


# LOCATIONS

@app.route('/api/locations', methods=['POST'])
@jwt_required()
def create_location():
    # Receiving Data
    new_location = Location.Location(request)
    response = new_location.add()
    return response


@app.route('/api/locations', methods=['GET'])
@jwt_required()
def get_locations():
    locations = db.locations.find()
    response = json_util.dumps(locations)
    json_dict = json_util.loads(response)
    i = 0
    for x in json_dict:
        json_dict[i]['_id'] = str(json_dict[i]['_id'])
        i = i + 1
    response = json_util.dumps(json_dict)
    return Response(response, mimetype="application/json")


@app.route('/api/locations/<id>', methods=['GET'])
@jwt_required()
def get_location(id):
    print(id)
    location = db.locations.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(location)
    return Response(response, mimetype="application/json")


@app.route('/api/locations/<id>', methods=['DELETE'])
@jwt_required()
def delete_location(id):
    db.locations.delete_one({'_id': ObjectId(id)})
    # TODO: do not delete if this location is used
    response = jsonify({'message': 'Location' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response



# TASKS
@app.route('/api/tasks', methods=['POST'])
@jwt_required()
def create_task():
    records = db.records.find()
    # Receiving Data
    name = request.json['name']
    link = request.json['link']
    level_id = request.json['level']['_id']
    rec_id = records[0]['_id']
    user_id = request.json['user_id']
    text = request.json['text']
    print(rec_id)
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
            'level_id': str(level_id),
            'rec_id': str(rec_id),
            'user_id': str(user_id),
            'text': text
        })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/api/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    current_user = get_jwt_identity()
    tasks = db.tasks.find()
    response = json_util.dumps(tasks)
    json_dict = json_util.loads(response)
    i = 0
    for x in json_dict:
        level = db.levels.find_one({'_id': ObjectId(x['level_id']), })
        json_dict[i]['level'] = {'_id': str(
            level['_id']), 'name': level['name']}
        json_dict[i]['_id'] = str(json_dict[i]['_id'])
        if 'level_id' in json_dict[i]:
            del json_dict[i]['level_id']
        i = i + 1
    response = json_util.dumps(json_dict)
    return Response(response, mimetype="application/json")


@app.route('/api/tasks/<id>', methods=['GET'])
@jwt_required()
def get_task(id):
    tasks = db.tasks.find({'_id': ObjectId(id), })
    response = json_util.dumps(tasks)
    json_dict = json_util.loads(response)
    i = 0

    for x in json_dict:
        level = db.levels.find_one({'_id': ObjectId(x['level_id']), })
        json_dict[i]['level'] = {'_id': str(
            level['_id']), 'name': level['name']}
        json_dict[i]['_id'] = str(json_dict[i]['_id'])
        if 'level_id' in json_dict[i]:
            del json_dict[i]['level_id']
        if 'user_id' in json_dict[i]:
            del json_dict[i]['user_id']
        if 'rec_id' in json_dict[i]:
            del json_dict[i]['rec_id']
        i = i + 1
    response = json_util.dumps(json_dict)
    return Response(response, mimetype="application/json")

@app.route('/api/tasks/info/<id>', methods=['GET'])
@jwt_required()
def get_task_info(id):
    tasks = db.tasks.find({'_id': ObjectId(id), })
    response = json_util.dumps(tasks)
    json_dict = json_util.loads(response)
    i = 0

    for x in json_dict:
        level = db.levels.find_one({'_id': ObjectId(x['level_id']), })
        json_dict[i]['level'] = {'_id': str(
            level['_id']), 'name': level['name']}

        user = db.users.find_one({'_id': ObjectId(x['user_id']), })
        json_dict[i]['username'] = user['username']
        
        json_dict[i]['_id'] = str(json_dict[i]['_id'])
        if 'level_id' in json_dict[i]:
            del json_dict[i]['level_id']
        if 'user_id' in json_dict[i]:
            del json_dict[i]['user_id']
        if 'rec_id' in json_dict[i]:
            del json_dict[i]['rec_id']
        i = i + 1
    response = json_util.dumps(json_dict)
    return Response(response, mimetype="application/json")


@app.route('/api/tasks/<id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    db.tasks.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Task' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/api/tasks/<_id>', methods=['PUT'])
@jwt_required()
def update_task(_id):
    name = request.json['name']
    link = request.json['link']
    level_id = request.json['level']['_id']
    rec_id = str(db.tasks.find_one({'_id': ObjectId(_id), })['rec_id'])
    user_id = str(db.tasks.find_one({'_id': ObjectId(_id), })['user_id'])
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
@jwt_required()
def create_record():
    # Receiving Data
    new_record = Record.Record(request)
    response = new_record.add()
    return response


@app.route('/api/records', methods=['GET'])
@jwt_required()
def get_records():
    records = db.records.find()
    response = json_util.dumps(records)
    json_dict = json_util.loads(response)
    i = 0
    for x in json_dict:
        json_dict[i]['_id'] = str(json_dict[i]['_id'])
        i = i + 1
    response = json_util.dumps(json_dict)
    return Response(response, mimetype="application/json")


@app.route('/api/records/<id>', methods=['GET'])
@jwt_required()
def get_record(id):
    print(id)
    record = db.records.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(record)
    return Response(response, mimetype="application/json")


@app.route('/api/records/<id>', methods=['DELETE'])
@jwt_required()
def delete_record(id):
    db.records.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Record' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/api/records/<_id>', methods=['PUT'])
@jwt_required()
def update_record(_id):
    new_record = Record.Record(request)
    response = new_record.update(_id)
    return response


# SESSIONS
@app.route('/api/sessions', methods=['POST'])
@jwt_required()
def create_session():
    # Receiving Data
    records = db.records.find()
    tasks = db.tasks.find()
    rec_id = str(records[0]['_id'])
    instructor_id = request.json['instructor_id']
    task_id = str(tasks[0]['_id'])
    user_id = "-"
    dtstart = request.json['dtstart']
    dtfinish = request.json['dtfinish']
    location = {"_id": request.json['location']['_id'], "name": request.json['location']['name']}

    if rec_id and instructor_id and task_id and user_id and dtstart and dtfinish and location:
        id = db.sessions.insert({
            'rec_id': rec_id,
            'instructor_id': instructor_id,
            'task_id': task_id,
            'user_id': user_id,
            'dtstart': dtstart,
            'dtfinish': dtfinish,
            'location': location
        })
        response = jsonify({
            '_id': str(id),
            'rec_id': rec_id,
            'instructor_id': instructor_id,
            'task_id': str(task_id),
            'user_id': str(user_id),
            'dtstart': dtstart,
            'dtfinish': dtfinish,
            'location': location
        })
        response.status_code = 201
        return response
    else:
        return not_found()




@app.route('/api/sessions', methods=['GET'])
@jwt_required()
def get_sessions():
    sessions = db.sessions.find()
    response = json_util.dumps(sessions)
    json_dict = json_util.loads(response)
    i = 0

    for x in json_dict:
        user = db.users.find_one({'_id': ObjectId(x['instructor_id']), })
        json_dict[i]['instructor'] = {"_id": str(user['_id']), "username": user['username']}

        if json_dict[i]['user_id'] != '-':
            user = db.users.find_one({'_id': ObjectId(x['user_id']), })
            json_dict[i]['user'] = {"_id": str(x['user_id']), "username": user['username']}
        else:
            json_dict[i]['user'] = {"_id": str(x['user_id']), "username": "-"}
        
        json_dict[i]['_id'] = str(json_dict[i]['_id'])
        if 'rec_id' in json_dict[i]:
            del json_dict[i]['rec_id']
        if 'task_id' in json_dict[i]:
            del json_dict[i]['task_id']
        if 'user_id' in json_dict[i]:
            del json_dict[i]['user_id']
        if 'instructor_id' in json_dict[i]:
            del json_dict[i]['instructor_id']
        i = i + 1
    response = json_util.dumps(json_dict)
    return Response(response, mimetype="application/json")


@app.route('/api/sessions/<id>', methods=['GET'])
@jwt_required()
def get_session(id):
    print(id)
    session = db.sessions.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(session)
    return Response(response, mimetype="application/json")


@app.route('/api/sessions/filter', methods=['GET'])
@jwt_required()
def get_my_sessions():
    # dtstart = datetime.strptime(request.json['dtstart'], date_format)
    # dtfinish = datetime.strptime(request.json['dtfinish'], date_format)
    location = request.json['location']
    # "dtstart": {"$gte": dtstart}, "dtfinish": {"$lte": dtfinish},
    sessions = db.sessions.find({"location": location})
    
    response = json_util.dumps(sessions)
    json_dict = json_util.loads(response)
    i = 0

    for x in json_dict:
        user = db.users.find_one({'_id': ObjectId(x['instructor_id']), })
        json_dict[i]['instructor'] = {"_id": str(user['_id']), "username": user['username']}

        if json_dict[i]['user_id'] != '-':
            user = db.users.find_one({'_id': ObjectId(x['user_id']), })
            json_dict[i]['user'] = {"_id": str(x['user_id']), "username": user['username']}
        else:
            json_dict[i]['user'] = {"_id": str(x['user_id']), "username": "-"}
        
        json_dict[i]['_id'] = str(json_dict[i]['_id'])
        if 'rec_id' in json_dict[i]:
            del json_dict[i]['rec_id']
        if 'task_id' in json_dict[i]:
            del json_dict[i]['task_id']
        if 'user_id' in json_dict[i]:
            del json_dict[i]['user_id']
        if 'instructor_id' in json_dict[i]:
            del json_dict[i]['instructor_id']
        i = i + 1
    response = json_util.dumps(json_dict)
    return Response(response, mimetype="application/json")


@app.route('/api/sessions/<id>', methods=['DELETE'])
@jwt_required()
def delete_session(id):
    db.sessions.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Session' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/api/sessions/<_id>', methods=['PUT'])
@jwt_required()
def update_session(_id):
    rec_id = str(db.sessions.find_one({'_id': ObjectId(_id), })['rec_id'])
    instructor_id = str(db.sessions.find_one({'_id': ObjectId(_id), })['instructor_id'])
    task_id = str(db.sessions.find_one({'_id': ObjectId(_id), })['task_id'])
    user_id = request.json['user_id']
    dtstart = str(db.sessions.find_one({'_id': ObjectId(_id), })['dtstart'])
    dtfinish = str(db.sessions.find_one({'_id': ObjectId(_id), })['dtfinish'])

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
@jwt_required()
def recieve_advice():
    new_advice = Advice.Advice(request)
    response = new_advice.get_advice()
    #response = json_util.dumps(result_data)
    return response


# BACK UP

@app.route('/api/backup', methods=['GET'])
@jwt_required()
def save_all():

    # Sessions
    a1 = db.sessions.find()
    res = json_util.dumps(a1)
    d1 = json_util.loads(res)

    a1 = db.levels.find()
    res = json_util.dumps(a1)
    d2 = json_util.loads(res)

    a1 = db.advice.find()
    res = json_util.dumps(a1)
    d3 = json_util.loads(res)

    a1 = db.records.find()
    res = json_util.dumps(a1)
    d4 = json_util.loads(res)

    a1 = db.tasks.find()
    res = json_util.dumps(a1)
    d5 = json_util.loads(res)

    a1 = db.users.find()
    res = json_util.dumps(a1)
    d6 = json_util.loads(res)


    ans = {'sessions' : d1, 'levels' : d2, 'advice' : d3, 'records' : d4, 'tasks' : d5, 'users' : d6}
    res = json_util.dumps(ans)

    return Response(res, mimetype="application/json")


@app.route('/api/create', methods=['GET'])  # TODO: take id
@jwt_required()
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
