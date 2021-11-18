from flask import Flask,Response,request
import bson.json_util as json_util
import redis
app = Flask(__name__)
from controller.movies_controller import MoviesController

#redis connection information
redis_cache = redis.Redis(host='localhost', port=6379, db=0)


#expiraton caching
@app.route('/set/<string:key>/<string:value>/<int:expired>')
def set_with_expiration(key, value, expired):
    redis_cache.set(key, value, ex=expired)
    return "OK"


#set caching
@app.route('/set/<string:key>/<string:value>')
def set_cache(key, value):
    if redis_cache.exists(key):
        return f"{key} already exists, use update instead"
    else:
        redis_cache.set(key, value)
        return "OK"

#update cached
@app.route('/update/<string:key>/<string:value>')
def update_cache(key, value):
    if redis_cache.exists(key):
        redis_cache.set(key, value)
        return "OK"
    else:
        return f"{key} does not exist"

#get cached
@app.route('/get/<string:key>')
def get_cache(key):
    if redis_cache.exists(key):
        redis_cache.get(key)
    else:
        return f"{key} does not exist"

#delete cached
@app.route('/delete/<string:key>')
def delete_cache(key):
    if redis_cache.exists(key):
        redis_cache.delete(key)
        return f"{key} deleted successfully"
    else:
        return f"{key} does not exist"


CONTENT_TYPE_HEADER = 'application/json'
controller = MoviesController()

@app.route("/", methods=['GET'])
def index():
    return Response(json_util.dumps("Welcome to the PAD2 lab!"), mimetype=CONTENT_TYPE_HEADER)

@app.route("/movies", methods=['GET'])
def get_movies():
    return Response(json_util.dumps(controller.get_all_movies()), mimetype=CONTENT_TYPE_HEADER)

@app.route("/movies/<id>", methods=['GET'])
def get_movie_by_id(id):
    return Response(json_util.dumps(controller.get_movie_by_id(id)), mimetype=CONTENT_TYPE_HEADER)

@app.route("/movies", methods=['PUT'])
def add_movie():
    return Response(json_util.dumps(controller.add_movie(request.get_json())), mimetype=CONTENT_TYPE_HEADER)

@app.route("/movies", methods=['POST'])
def update_movie():
    return Response(json_util.dumps(controller.update_movie(request.get_json())), mimetype=CONTENT_TYPE_HEADER)

@app.route("/movies", methods=['DELETE'])
def delete_movie():
    return Response(json_util.dumps(controller.delete_movie(request.get_json())), mimetype=CONTENT_TYPE_HEADER)

if __name__ == '__main__':
    app.run(debug=True)


