from repository.movies_repo import MoviesRepo
from model.movie import Movie
class MoviesController:
    def __init__(self):
        self.repo = MoviesRepo()
        
    def __movie_exists(self, movie_id):
        exist = self.get_movie_by_id(movie_id)
        if exist == {}:
            return False
        return True    
    
    def get_all_movies(self):
        res = []
        for movie in self.repo.get_all():
            res.append(movie)
            # print(movie)
        return res
    
    def get_movie_by_id(self, id):  
        res = self.repo.get_by_id(id)
        if not res:
            return {}
        return res

    def update_movie(self, movie_json):
        if not self.__is_movie_json_valid(movie_json,False):
            return {'error' : 'idi v zhopy debil NETY POLEI NYZHNIH SALYAM ALEYKUM'}
        
        movie = Movie()
        movie.set_id(movie_json['id'])
        movie.set_title(movie_json['title'])
        movie.set_description(movie_json['description'])
        
        # if movie exists
        if not self.__movie_exists(movie.get_id()):
            return {'error' : 'idi v zhopy debil net etogo myvika y nas'}
        res = self.repo.update(movie)
        if res.matched_count > 0:
            return self.get_movie_by_id(movie.get_id())
        return {'error' : 'error during updating movie'}
    
    def add_movie(self,movie_json):
        if not self.__is_movie_json_valid(movie_json,True):
            return {'error' : 'wrong or no field specified'}
        
        movie = Movie()
        movie.generate_id()
        movie.set_title(movie_json['title'])
        movie.set_description(movie_json['description'])
        
        if self.__movie_exists(movie.get_id()):
            return {'error' : 'movie with this id already exists'}
        res = self.repo.create(movie)
        if res.inserted_id:
            return self.get_movie_by_id(movie.get_id())
        return {'error' : 'error during movie creation'}
    
    def delete_movie(self, movie_json):
        if not movie_json['id']:
            return {'error' : 'id was not specified'}
        if not self.__movie_exists(movie_json['id']):
            return {'error' : 'movie with this id doesn\'t exist'}
        res = self.repo.delete(movie_json['id'])
        if res.deleted_count > 0:
            return {'msg': 'movie successfully deleted'}
        return {'error' : 'error during movie deletion'}
    
    # util
    def __is_movie_json_valid(self, json,is_create):
        if is_create == False:
            if json is None or not json['id']:
                return False
        if not json['title'] or not json['description']:
            return False
        return True
