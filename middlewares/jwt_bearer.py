from fastapi.security import HTTPBearer #esta clase se utiliza para la validación y con esta se crea una nueva clase JWTBearer
from fastapi import Request, HTTPException
from jwt_manager import create_token, validate_token

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request) #esta función es requerida para acceder a la petición del usuario y esta función requiere de la petición
    #super llama la clase superior, en este caso es la del parámetro HHTPBearer... __call__ está en el módulo HTTP.PY
    #Es una función asincrona y va a demorar un poco, por eso se llama async def y return await
        data = validate_token(auth.credentials)
        if data["email"] != "admin@gmail.com": #si esto es correcto, entoces se lanza una excepción 
            raise HTTPException(status_code=403, detail="Credenciales son inválidas")