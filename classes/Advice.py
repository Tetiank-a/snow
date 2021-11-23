from flask.json import jsonify
from predict.add import predict

class Advice:
    def __init__(self, request):
        self.advice = request.json['advice']

    def get_advice(self):
        response = jsonify({'message': predict()}) # TODO: pass coordinates and angle
        response.status_code = 200
        return response