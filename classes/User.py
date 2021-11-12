import re
from bson.objectid import ObjectId

from flask.json import jsonify
from werkzeug.security import generate_password_hash
import main


class User:

    valid = True

    def __init__(self, request):
        if (('username' in request.json) and ('email' in request.json) and
                ('level_id' in request.json) and ('password' in request.json)):
            self.username = request.json['username']
            self.email = request.json['email']
            self.level_id = request.json['level_id']
            self.password = request.json['password']
        else:
            self.valid = False

    def isValid(self):
        if not self.valid:
            response = jsonify({'message': 'One or more fields are not sent'})
            response.status_code = 400
            return response
        if not (self.username and self.email and self.level_id and self.password):
            response = jsonify({'message': 'All fields must be set'})
            response.status_code = 400
            return response
        # email validation
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        response = jsonify({'message': 'User is valid'})
        response.status_code = 201
        if(not re.fullmatch(regex, self.email)):
            response = jsonify({'message': 'Invalid email'})
            response.status_code = 400
        if not ObjectId.is_valid(self.level_id):
            response = jsonify({'message': 'level_id is not a valid ObjectId'})
            response.status_code = 400
        else:
            level = main.db.levels.find_one({'_id': ObjectId(self.level_id), })
            if not level:
                response = jsonify({'message': 'Such level does not exist'})
                response.status_code = 400
        if len(self.password) < 8 or len(self.password) > 30:
            response = jsonify(
                {'message': 'Password must be longer than 8 symbols, but less than 30'})
            response.status_code = 400
        if len(self.username) < 2 or len(self.username) > 20:
            response = jsonify(
                {'message': 'Username must be longer than 2 symbols, but less than 20'})
            response.status_code = 400
        return response

    def add(self):
        response = self.isValid()
        if not (response.status_code == 400):
            self.password = generate_password_hash(self.password)
            self.id = main.db.users.insert(
                {'username': self.username, 'email': self.email,
                 'level_id': self.level_id, 'password': self.password})
            response = jsonify({
                '_id': str(self.id),
                'username': self.username,
                'password': self.password,
                'email': self.email,
                'level_id': str(self.level_id)
            })
        return response

    def update(self, _id):
        response = self.isValid()
        if not _id:
            return main.not_found()
        if not (response.status_code == 400):
            self.password = generate_password_hash(self.password)
            main.db.users.update_one(
                {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {
                    'username': self.username,
                    'email': self.email,
                    'level_id': self.level_id,
                    'password': self.hashed_password
                }
                })
            response = jsonify(
                {'message': 'User' + _id + 'Updated Successfuly'})
            response.status_code = 200
        return response
