from FaceMatcher import faceMatcher
from flask_restx import Api, Resource, reqparse
import json
from flask import Flask, Response



app = Flask(__name__)

api = Api(app)

def make_response(response,status_code):
    request_response = {}
    request_response['response'] = response
    ret  = json.dumps(request_response)
    res =  Response(ret, status=status_code, mimetype='application/json')
    res.headers.add("Access-Control-Allow-Origin", "*")
    return res

register_parser = reqparse.RequestParser()
register_parser.add_argument('image', location='json',
                        type=list, required=True)

match_parser = register_parser.copy()
register_parser.add_argument('uid', required=True, 
                    location='form')

@api.route('/registerface')
@api.expect(register_parser, validate = True)
class RegisterFace(Resource):
    def post(self):
        args = register_parser.parse_args()
        uid = args['uid']
        image = args['image'].read()
        return make_response(faceMatcher.addFace(uid,image),200)

@api.route('/matchface')
@api.expect(match_parser, validate = True)
class MatchFace(Resource):
    def post(self):
        args = match_parser.parse_args()
        image = args['image'].read()
        return make_response(faceMatcher.matchFace(image),200)
        

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=9999)


