from fastapi import APIRouter
from pydantic import BaseModel
from jwt_manager import create_token
from fastapi.responses import JSONResponse
from schemas.user import User

user_router = APIRouter()


@user_router.post("/login/", tags=["auth"]) #ruta
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin": #esto es para simular
        token: str = create_token(user.dict()) #se debe enviar la data del usuario convertida en diccionario y se puede guardar en una variable
        return JSONResponse(status_code=200, content=token) #la respuesta es un código de estado y el content es lo que se genere en la variable token

 #El response_model como parámetro de la clase get_movies, devuelve o genera una lista de películas [Movie] 