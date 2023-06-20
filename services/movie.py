from models.movie import Movie as MovieModel
from schemas.movie import Movie
from fastapi import Depends, Path, Query

class MovieService():

    def __init__(self, db) -> None:  #Método consultor yo voy a requerir que cada vez que se llame este servicio se le envíe una sesion a la base de datos
        self.db = db  #db #es la sesion que está llegando

    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result   

    def get_movie(self, id):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result 
    
    def get_movies_by_category(self, category):
        result = self.db.query(MovieModel).filter(MovieModel.category == category).first()
        return result
    
    def create_movie(self, movie: Movie):
        new_movie = MovieModel(**movie.dict())    #Esta parte es para enviar la película al sqlite
        self.db.add(new_movie)
        self.db.commit()    #Esto guarta el dato
        return
    
    def update_movie(self, id: int, data: Movie):
        movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        movie.title = data.title
        movie.overview = data.overview
        movie.year = data.year
        movie.rating = data.rating
        movie.category = data.category
        self.db.commit()
        return
    
    def delete_movie(self, id: int):
        self.db.query(MovieModel).filter(MovieModel.id == id).delete()
        self.db.commit()
        return

    

    #Este servicio debe ser importado en el router de películas