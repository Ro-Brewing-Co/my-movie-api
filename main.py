from fastapi import FastAPI, Depends, Body, HTTPException, Path, Query, Request #La clase Body se importa para que no sean parámetros tipo query, sino que se puedan modificar en la documentación...como objeto
from fastapi.responses import HTMLResponse, JSONResponse #Para responder con código HTML
from pydantic import BaseModel, Field #BaseModel permite crear esquemas#Para añadir validaciones debemos importar una clase que se llama Field y se importa desde pydantic
from typing import Optional, List #Esto para dar opcion en la clase Movie el id la requiere. La clase List es para generar respuestas en listas.
from pyjwt import create_token, validate_token #Se importa la función de pyjwt.py con nombre create_token 
from fastapi.security import HTTPBearer #esta clase se utiliza para la validación y con esta se crea una nueva clase JWTBearer



#Aquí se crea la aplicación
app = FastAPI()
#Para cambiar el titulo fastapi de /docs:
app.title = "Mi aplicación con FastAPI"
#Para cambiar la versión, que son los números que acompañan como potencia al título:
app.version = "0.0.1"

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request) #esta función es requerida para acceder a la petición del usuario y esta función requiere de la petición
    #super llama la clase superior, en este caso es la del parámetro HHTPBearer... __call__ está en el módulo HTTP.PY
    #Es una función asincrona y va a demorar un poco, por eso se llama async def y return await
        data = validate_token(auth.credentials)
        if data["email"] != "admin@gmail.com": #si esto es correcto, entoces se lanza una excepción 
            raise HTTPException(status_code=403, detail="Credenciales son inválidas")


class User(BaseModel):
    email: str
    password: str

#Creamos una classe que herdeda BaseModel 
class Movie(BaseModel): #Dentro de esta clase metemos todos los atributos que lleva una película
    id: Optional[int] = None #Llamamos o importamos optional de tiping que viene con fastapi. Esto para dar opcion de que sea entero o none.
    title: str = Field(min_length=5, max_length=15) #Aquí se realiza una validación con la clase importada Field
    overview: str = Field(default="Esta película no tiene overview", min_length=15, max_length=50)                       #El default es un valor por defecto... 
    year: int  = Field(le=2022) #El le es para limitar hasta, en este caso, va hastaa el 2022
    rating: float = Field(default=10, ge=1, le=10)
    category: str = Field(default='Categoría', min_length=5, max_length=15)

    class config(): #No está funcionando y no ha sido posible encontrar el error
        schema_extra = { 
            "example": {
                "id": 1,
                "title": "Mi película",
                "overview": "Descripción de la película",
                "year": 2022,
                "rating": 9.8,
                "category": "Acción"
                }
            }

#Esto no es necesario citarlo, ya se aplica directamente en la documentación
#Para eliminar el default creamos una clase:
    
#Aquí se agregan diccionarios con la información de las películas
 #Nombre del diccionario
movies  = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exberante palaneta llamado Pandora viven los Na´vi...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    },
    {
        "id": 2,
        "title": "Avatar",
        "overview": "En un exberante palaneta llamado Pandora viven los Na´vi...",
        "year": "2009",
        "rating": 9.8    ,
        "category": "Acción"
    }
]
#Ahora el primer endpoint
@app.get("/", tags = ["Home"])
#la función que se va a ejecutar es la siguiente:
def message():
    return HTMLResponse("<h1>Hello world!</h1>") #Este devuelve un HTML como un <h1> mensaje que quiero que aparezca</h1> Aparece en localhost:5000
    #return {"Hello": "world"} #Esto retorna un diccionario

@app.post("/login/", tags=["auth"]) #ruta
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin": #esto es para simular
        token: str = create_token(user.dict()) #se debe enviar la data del usuario convertida en diccionario y se puede guardar en una variable
        return JSONResponse(status_code=200, content=token) #la respuesta es un código de estado y el content es lo que se genere en la variable token

 #El response_model como parámetro de la clase get_movies, devuelve o genera una lista de películas [Movie] 
@app.get("/movies/", tags=["movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())]) #Esto es para agregar películas... /movies es la dirección y tags es la etiqueta, aparece así en la aplicación
def get_movies() -> List[Movie]:
   return JSONResponse(status_code=200, content=movies) #content es el contenido que se le pide enviar. 

@app.get("/movies/{id}", tags=["movies"], response_model=Movie) 
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie: 
    for item in movies:  
        if item["id"] == id: #si el item(id) es igual a lo que se busca (id), entonces...
            return JSONResponse(content=item) #Return ese item, el id
    return JSONResponse(status_code=404, content=[]) #Esto debe retornar [] si no es válido lo que se ingresa o no encuentra el número, el item




@app.get("/movies", tags=["movies"], response_model=List[Movie])
def get_movies_by_category(category: str =  Query(min_length=5, max_length=15)) -> List[Movie]:
    data = [item for item in movies if item["category"] == category]#El parámetro no debe estar en la línea @app.get... eso es parámetro Path
            #El Query funciona sin el parámetro Path, 
    return JSONResponse(content=data)   

@app.post("/movies", tags=["movies"], response_model=dict, status_code=201)   #Aquí la respuesta será un diccionario
def create_movie(movie: Movie) -> dict:
   movies.append(movie) #esto permite la inserción de datos... El body fue reemplazado por la clase movie, por eso se quitan todo s los bodys y el diccionario
   return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"}) #Para que no se vea en la aplicación como parámetros query, si no que aparezcan en el body, se debe importar la clase Body de Fastapi
                #Ahora se le ha cambiado el title por movies, luego lo que reorna es un listado actualizado

@app.put("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict: #De igual manera que en post, se quitan los bodys por la clase Movie, queda id porque se requiere para actualización por filtración
    for item in movies: #Los demás están en BODY para modificarlos en una caja
        if item["id"] == id: #id no requiere body porque filtramos a partir de este y sería un parámetro path ya que está en los parámetros de la función
            item["title"] = movie.title #Luego, la película que se modificará, es la que tenga el id asignado que es la única que se modifica
            item["overview"] = movie.overview
            item["year"] = movie.year                   #SIN COMAS
            item["rating"] = movie.rating
            item["category"] = movie.category  #Se pone movie.item porque se debe llamar desde la clase Movie
            return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"}) #retorna la nueva lista de películas... si no se pone esto, no muestra la nueva lista
        
@app.delete("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
def delete_movie(id: int)-> dict: #Solo se vusca por el id.
    for item in movies: #Esto recorre el listado de películas buscando el id que se introduce, cuando lo encuentra aplica el movies.remove y la borra
        if item["id"] == id:
            movies.remove(item) #este método borra el item encontrado como id 
            return JSONResponse(status_code=200, content={"message": "Se ha eliminado la película"}) #Retorna el listado de películas actualizado

