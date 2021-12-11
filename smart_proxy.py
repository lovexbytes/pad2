from flask import Flask,Response,request
import bson.json_util as json_util
import redis
import requests

app = Flask(__name__)

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_TTL = 60

CONTENT_TYPE_HEADER = 'application/json'
SERVER_LINK = 'http://localhost:8000/'


redis_cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

def get_cached_or_send_request(key,http_method,json_string):
    # print(key,http_method,json_string)
    if redis_cache.exists(key):
        return redis_cache.get(key).decode('utf-8') + "from redis with love"
    if json_string:
        response = getattr(requests, http_method)(SERVER_LINK + key, json=json_string)
    else:
        response = getattr(requests, http_method)(SERVER_LINK + key)
    # response = requests.get(SERVER_LINK + '/movies')
    result = response.json()
    set_cached(key,result)
    return result


def set_cached(key, value):
    redis_cache.setex(key, REDIS_TTL, str(value))


def get_json_response(value):
    return Response(json_util.dumps(value), mimetype=CONTENT_TYPE_HEADER)

@app.route("/", methods=['GET'])
def index():
    return get_json_response('Welcome to the smart proxy!')

@app.route("/movies", methods=['GET'])
def get_movies():  
    return get_json_response(get_cached_or_send_request('movies','get', None))

@app.route("/movies/<id>", methods=['GET'])
def get_movie_by_id(id):
    return get_json_response(get_cached_or_send_request("movies/" + str(id),'get', None))

@app.route("/movies", methods=['PUT'])
def add_movie():
    response = requests.put('movies',json=request.get_json())
    return get_json_response(response.json())

@app.route("/movies", methods=['POST'])
def update_movie():
    key = 'movies/' + request.get_json()['id']
    if redis_cache.exists(key):
        redis_cache.delete(key)
    return get_json_response(get_cached_or_send_request(key, "post",request.get_json()))

@app.route("/movies", methods=['DELETE'])
def delete_movie():
    response = requests.delete('movies', json=request.get_json())
    return get_json_response(response.json())

if __name__ == '__main__':
    app.run(debug=True, port=8001)


