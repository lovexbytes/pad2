from flask import Flask,Response,request
import bson.json_util as json_util
app = Flask(__name__)
from controller.movies_controller import MoviesController




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


