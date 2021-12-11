from flask import Flask,Response,request
import bson.json_util as json_util
app = Flask(__name__)
from controller.movies_controller import MoviesController

CONTENT_TYPE_HEADER = 'application/json'
controller = MoviesController()

def call_method(method_name, *args):
    return getattr(controller, method_name)(*args)
    
def get_json_response(value):
    return Response(json_util.dumps(value), mimetype=CONTENT_TYPE_HEADER)

@app.route("/", methods=['GET'])
def index():
    return get_json_response("Welcome to the PAD2 lab!")

@app.route("/movies", methods=['GET'])
def get_movies():    
    return get_json_response(call_method("get_all_movies"))

@app.route("/movies/<id>", methods=['GET'])
def get_movie_by_id(id):
    return get_json_response(call_method("get_movie_by_id",id))

@app.route("/movies", methods=['PUT'])
def add_movie():
    return get_json_response(controller.add_movie(request.get_json()))

@app.route("/movies", methods=['POST'])
def update_movie():
    if not controller.is_movie_json_valid(request.get_json(),False):
        return {'error' : 'no required fields given'}
    return get_json_response(call_method("update_movie",request.get_json()))

@app.route("/movies", methods=['DELETE'])
def delete_movie():
    return get_json_response(controller.delete_movie(request.get_json()))

if __name__ == '__main__':
    app.run(debug=True, port=8000)


