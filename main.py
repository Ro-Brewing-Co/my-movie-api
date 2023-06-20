from fastapi import FastAPI #La clase Body se importa para que no sean parámetros tipo query, sino que se puedan modificar en la documentación...como objeto
from fastapi.responses import HTMLResponse, JSONResponse #Para responder con código HTML
from pydantic import BaseModel #BaseModel permite crear esquemas#Para añadir validaciones debemos importar una clase que se llama Field y se importa desde pydantic
 #Esto para dar opcion en la clase Movie el id la requiere. La clase List es para generar respuestas en listas.
from jwt_manager import create_token #Se importa la función de pyjwt.py con nombre create_token 
from config.database import engine, Base #Esto está  importado de la carpeta config  y es el motor...
from models.movie import Movie as MovieModel #Esta función es la de la carpeta models y es para la creación de tablas
#Se le cambia el nombre de improtación a movie porque en este archivo hay otra clase con ese nombre.
from routers.movie import movie_router #aquí se imprta el módilo que contiene el router.py
from middlewares.error_handler import ErrorHandler
from routers.user import user_router



#Aquí se crea la aplicación
app = FastAPI()
#Para cambiar el titulo fastapi de /docs:
app.title = "Mi aplicación con FastAPI"
#Para cambiar la versión, que son los números que acompañan como potencia al título:
app.version = "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(movie_router)  
app.include_router(user_router)   #Esto es para incluir y llamar a los routers creados en router carpeta

'''
Aquí se incluye el router que creamos en la carpeta módulo router...recuerda que __init__.py es para que python reconozca 
la carpeta router como módulo, cada carpeta que quiera esa condicion, debe tener ese init en su interior.

'''
Base.metadata.create_all(bind=engine) #Aquí se está importando el motor para la base de datos 





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


