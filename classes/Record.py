from bson.objectid import ObjectId

from flask.json import jsonify
import main


class Record:

    valid = True

    def __init__(self, request):
        if (('xspeed' in request.json) and ('yspeed' in request.json) and
                ('zspeed' in request.json) and ('angle' in request.json)):
            self.xspeed = request.json['xspeed']
            self.yspeed = request.json['yspeed']
            self.zspeed = request.json['zspeed']
            self.angle = request.json['angle']
        else:
            self.valid = False

    def isValid(self):
        if not self.valid:
            response = jsonify({'message': 'One or more fields are not sent'})
            response.status_code = 400
            return response
        if not (self.xspeed and self.yspeed and self.zspeed):
            response = jsonify({'message': 'All fields must be set'})
            response.status_code = 400
            return response

        response = jsonify({'message': 'User is valid'})
        response.status_code = 201
        if not (isfloat(self.xspeed) and isfloat(self.yspeed) and
                isfloat(self.zspeed) and isfloat(self.angle)):
            response = jsonify({'message': 'Values must be float numbers'})
            response.status_code = 400

        return response

    def add(self):
        response = self.isValid()
        if not (response.status_code == 400):
            if self.xspeed and self.yspeed and self.zspeed and self.angle:
                self.id = main.db.records.insert({
                    'xspeed': [self.xspeed, ],
                    'yspeed': [self.yspeed, ],
                    'zspeed': [self.zspeed, ],
                    'angle': [self.angle, ]
                })
                response = jsonify({
                    '_id': str(self.id),
                    'xspeed': self.xspeed,
                    'yspeed': self.yspeed,
                    'zspeed': self.zspeed,
                    'angle': self.angle
                })
                response.status_code = 201

        return response

    def update(self, _id):
        response = self.isValid()
        if not (response.status_code == 400):
            if not _id:
                return main.not_found()
            if self.xspeed and self.yspeed and self.zspeed and self.angle:
                main.db.records.update_one(
                    {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$push': {
                        'xspeed': self.xspeed,
                        'yspeed': self.yspeed,
                        'zspeed': self.zspeed,
                        'angle': self.angle
                    }})
                response = jsonify(
                    {'message': 'Record' + _id + 'Updated Successfuly'})
                response.status_code = 200

        return response


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
