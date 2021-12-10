from flask import Flask,Response,request
import bson.json_util as json_util
import redis
app = Flask(__name__)
from controller.movies_controller import MoviesController

redis_cache = redis.Redis(host='localhost', port=6379, db=0)
CONTENT_TYPE_HEADER = 'application/json'
controller = MoviesController()

def get_cached_or_call_method(key, method_name, *args):
    if redis_cache.exists(key):
        return redis_cache.get(key).decode('utf-8') + "from redis with love"
    value = getattr(controller, method_name)(*args)
    redis_cache.setex(key, 60, str(value))
    return value
    
def get_json_response(value):
    return Response(json_util.dumps(value), mimetype=CONTENT_TYPE_HEADER)

@app.route("/", methods=['GET'])
def index():
    return get_json_response("Welcome to the PAD2 lab!")

@app.route("/movies", methods=['GET'])
def get_movies():    
    return get_json_response(get_cached_or_call_method("movies", "get_all_movies"))

@app.route("/movies/<id>", methods=['GET'])
def get_movie_by_id(id):
    return get_json_response(get_cached_or_call_method("movies/" + str(id), "get_movie_by_id",id))

@app.route("/movies", methods=['PUT'])
def add_movie():
    return get_json_response(controller.add_movie(request.get_json()))

@app.route("/movies", methods=['POST'])
def update_movie():
    if not controller.is_movie_json_valid(request.get_json(),False):
        return {'error' : 'no required fields given'}
    
    key = 'movies/update/' + request.get_json()['id']
    
    if redis_cache.exists(key):
        redis_cache.delete(key)
    return get_json_response(get_cached_or_call_method(key, "update_movie",request.get_json()))

@app.route("/movies", methods=['DELETE'])
def delete_movie():
    return get_json_response(controller.delete_movie(request.get_json()))

if __name__ == '__main__':
    app.run(debug=True, port=8001, threaded=True)


