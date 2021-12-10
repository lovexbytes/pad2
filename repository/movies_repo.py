from util.database_controller import DatabaseController
import bson.json_util as json_util
movies = [
    {   
        'id':'1',
        'title':'titanic',
        'desc':'DiCaprio freezes',
    },
]

class MoviesRepo:
    def __init__(self):
        self.__dbc = DatabaseController()
    
    def get_all(self):
        return self.__dbc.get_connection().find({},{'_id':False})
    
    def get_by_id(self, id):
        return self.__dbc.get_connection().find_one({'id':id},{'_id':False})
    
    def get_by_title(self, title):
        return self.__dbc.get_connection().find_one({'title':title},{'_id':False})
    
    def update(self, movie):
        id_query = { "id": movie.get_id() }
        new_value = { "$set": { "title": movie.get_title(), "description": movie.get_description()} }

        return self.__dbc.get_connection().update_one(id_query, new_value, upsert=False)
    
    def create(self, movie):
        print(json_util.dumps(movie.__dict__))
        return self.__dbc.get_connection().insert_one(json_util.loads(json_util.dumps(movie.__dict__)))

    
    def delete(self, id):
        return self.__dbc.get_connection().delete_one({'id':id})