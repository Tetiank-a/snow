import re
from bson.objectid import ObjectId

from flask.json import jsonify
from werkzeug.security import generate_password_hash
import main


class Level:

    def __init__(self, request):
        self.name = request.json['name']

    def isValid(self):
        if not (self.name):
            response = jsonify({'message': 'All fields must be set'})
            response.status_code = 400
            return response
        response = jsonify({'message': 'Level is valid'})
        response.status_code = 201
        return response

    def add(self):
        response = self.isValid()
        if not (response.status_code == 400):
            self.id = main.db.levels.insert(
                {'name': self.name})
            response = jsonify({
                '_id': str(self.id),
                'name': self.name
            })
        return response

    def update(self, _id):
        response = self.isValid()
        if not _id:
            return main.not_found()
        if not (response.status_code == 400):
            main.db.levels.update_one(
                {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {
                    'name': self.name
                }
                })
            response = jsonify(
                {'message': 'Level' + _id + 'Updated Successfuly'})
            response.status_code = 200
        return response
