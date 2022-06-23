from bson.objectid import ObjectId
from flask.json import jsonify
from predict.add import predict2
import app.main


class Advice:
    def __init__(self, request):
        self.record_id = request.json['record_id']
        self.time = request.json['time']

    def get_advice(self):
        record = app.main.db.records.find_one({'_id': ObjectId(self.record_id), })
        if not record:
            response = jsonify({'message': 'Such record does not exist'})
            response.status_code = 400
            return response
        i = int(self.time)
        response = jsonify({'message': str(predict2(float(record['xspeed'][i]),
                                                   float(record['yspeed'][i]),
                                                   float(record['zspeed'][i]),
                                                   int(record['angle'][i]),
                                                   float(record['point_left_front'][i]),
                                                   float(record['point_left_back'][i]),
                                                   float(record['point_right_front'][i]),
                                                   float(record['point_right_back'][i])))})
        response.status_code = 200
        return response
