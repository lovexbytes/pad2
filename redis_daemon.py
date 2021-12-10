from flask import Flask,Response,request
import bson.json_util as json_util
import redis
import requests
app = Flask(__name__)
LINK_TO_CORE = 'http://localhost:5000/'

#redis connection information
redis_cache = redis.Redis(host='localhost', port=6379, db=0)


#expiraton caching
@app.route()
def set_with_expiration(key, value, expired):
    redis_cache.set(key, value, ex=expired)
    return "OK"


#set caching
@app.route()
def set_cache(key, value):
    if redis_cache.exists(key):
        return f"{key} already exists, use update instead"
    else:
        redis_cache.set(key, value)
        return "OK"

#update cached
@app.route()
def update_cache(key, value):
    if redis_cache.exists(key):
        redis_cache.set(key, value)
        return "OK"
    else:
        return f"{key} does not exist"

#get cached
@app.route()
def get_cache(key):
    if redis_cache.exists(key):
        redis_cache.get(key)
    else:
        return f"{key} does not exist"

#delete cached
@app.route()
def delete_cache(key):
    if redis_cache.exists(key):
        redis_cache.delete(key)
        return f"{key} deleted successfully"
    else:
        return f"{key} does not exist"


CONTENT_TYPE_HEADER = 'application/json'



#response function
def resp_func(key):
    if redis_cache.exists(key):
        return redis_cache.get(key).decode('utf-8') + "from redis with love"
    else:
        value = str(requests.get(LINK_TO_CORE + key).text)
        print (value)
        redis_cache.setex(key, 60, value)
        return value

#redis PUT
def resp_add(key):
    if redis_cache.exists(key):
        return redis_cache.get(key).decode('utf-8')
    else:
        return

#redis POST
def resp_update(key):
    if redis_cache.exists(key):
        return redis_cache.get(key).decode('utf-8')
    else:
        return

#redis DELETE
def resp_delete(key):
    if redis_cache.exists(key):
        return redis_cache.get(key).decode('utf-8')
    else:
        return




@app.route("/", methods=['GET'])
def index():
    return Response("",mimetype=CONTENT_TYPE_HEADER)

@app.route("/movies", methods=['GET'])
def get_movies():
    return Response(json_util.dumps(resp_func('movies')),mimetype=CONTENT_TYPE_HEADER)

@app.route("/movies/<id>", methods=['GET'])
def get_movie_by_id(id):
    return Response(json_util.dumps(),mimetype=CONTENT_TYPE_HEADER)

@app.route("/movies", methods=['PUT'])
def add_movie():
    return Response(json_util.dumps(resp_add()), mimetype=CONTENT_TYPE_HEADER)

@app.route("/movies", methods=['POST'])
def update_movie():
    return Response(json_util.dumps(resp_update()), mimetype=CONTENT_TYPE_HEADER)

@app.route("/movies", methods=['DELETE'])
def delete_movie():
    return Response(json_util.dumps(resp_delete()), mimetype=CONTENT_TYPE_HEADER)

if __name__ == '__main__':
    app.run(debug=True, port=5001)


