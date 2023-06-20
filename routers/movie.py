from fastapi import APIRouter
from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from typing import Optional, List #Esto para dar opcion en la clase Movie el id la requiere. La clase List es para generar respuestas en listas.
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter() 
'''
Es como si se estuviera creando una aplicación, pero ya a nivel de router...se toman de main.py todas 
las rutas que tengan que ver con movie y se traen a este mmódulo para luego llamarlas de nuevo como @movie_router.
Se trae esquema que es class Movie(BaseModel)...se traen los from que sean necesarios y se debe llamar este módulo en 
el archivo principal que es main.py
'''


@movie_router.get("/movies/", tags=["movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())]) #Esto es para agregar películas... /movies es la dirección y tags es la etiqueta, aparece así en la aplicación
def get_movies() -> List[Movie]:
    db = Session()  #Se llama la función session para enlazarse a la base de datos
    result = MovieService(db).get_movies()  #db es la variable, es session  y debe devolver una lista query del la...all para que muestre todo
    return JSONResponse(status_code=200, content=jsonable_encoder(result)) #content es el contenido que se le pide enviar. Aquí se cambia a content=result

@movie_router.get("/movies/{id}", tags=["movies"], response_model=Movie) 
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie: 
    db = Session()   #Par el filtrado por id también se debe crear una session
    result = MovieService(db).get_movie(id)  
    #Explicación a anterior línea: Con la sesion se ejecuta un query que es ejecutado al modelo de películas y luego con el .finter se filtra 
    #laMovieModel por id y el first() muestra la primera coincidencia
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result)) #Esto debe retornar [] si no es válido lo que se ingresa o no encuentra el número, el item




@movie_router.get("/movies", tags=["movies"], response_model=List[Movie])
def get_movies_by_category(category: str =  Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()   #Par el filtrado por id también se debe crear una session
    result = MovieService(db).get_movies_by_category(category)
    #El parámetro no debe estar en la línea @app.get... eso es parámetro Path
            #El Query funciona sin el parámetro Path, 
    return JSONResponse(status_code=200, content=jsonable_encoder(result))   

@movie_router.post("/movies", tags=["movies"], response_model=dict, status_code=201)   #Aquí la respuesta será un diccionario
def create_movie(movie: Movie) -> dict:
   db = Session()   #Con esyta variable se crea el enlace con basededatos, se crea la session
   MovieService(db).create_movie(movie) #Aquí se le pasa a la base de datos database.py la información que se quiere registrar
   #**movie.dict con asteriscos para que se pase como un parámetro...esto crea la película ya que viene de movie y lo pasa como diccionario
   #Desde la base de datos se añade con .app la película que se acaba de crear
   #Actualización para que los cambios se guarden
   #movies.append(movie) #esto permite la inserción de datos... El body fue reemplazado por la clase movie, por eso se quitan todo s los bodys y el diccionario
   #La anterior fila se elmina ya que las dos líneas anteriores a esta hacen lo mismo.
   return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"}) #Para que no se vea en la aplicación como parámetros query, si no que aparezcan en el body, se debe importar la clase Body de Fastapi
                #Ahora se le ha cambiado el title por movies, luego lo que reorna es un listado actualizado

@movie_router.put("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict: #De igual manera que en post, se quitan los bodys por la clase Movie, queda id porque se requiere para actualización por filtración
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"}) #retorna la nueva lista de películas... si no se pone esto, no muestra la nueva lista
        
@movie_router.delete("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def delete_movie(id: int)-> dict: #Solo se vusca por el id.
    db = Session()
    result: MovieModel = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado la película"}) #Retorna el listado de películas actualizado

