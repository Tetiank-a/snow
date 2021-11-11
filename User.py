import re
from bson.objectid import ObjectId

from flask.json import jsonify
from werkzeug.security import generate_password_hash
# from .main import db


class User:

    def __init__(self, request):
        self.username = request.json['username']
        self.email = request.json['email']
        self.level_id = request.json['level_id']
        self.password = request.json['password']


    def isValid(self, db):
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
            level = db.levels.find_one({'_id': ObjectId(self.level_id), })
            if not level:
              response = jsonify({'message': 'Such level does not exist'})
              response.status_code = 400
        if len(self.password) < 8 or len(self.password) > 30:
            response = jsonify({'message': 'Password must be longer than 8 symbols, but less than 30'})
            response.status_code = 400
        if len(self.username) < 2 or len(self.username) > 20:
            response = jsonify({'message': 'Username must be longer than 2 symbols, but less than 20'})
            response.status_code = 400
        return response


    def transform(self, db):
        response = self.isValid(db)
        if (response.status_code == 201):
            self.password = generate_password_hash(self.password)
        return response