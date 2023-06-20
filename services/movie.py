from models.movie import Movie as MovieModel

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
    

    #Este servicio debe ser importado en el router de películas