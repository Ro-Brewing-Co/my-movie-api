from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

class ErrorHandler(BaseHTTPMiddleware):       #Método constructor 
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)             #El método super hace referencia al que está en la clase como parámetro el BaseHTTPMiddleware 
        

                               
    async def dispatch(self, request: Request, call_next) -> Response or JSONResponse:                 #este metodos se va a ejecutar para estar detectado errores en la aplicación
        try:                 #represetna la siguinete llamada, en caso de que no ocurra un error, contiúna a la siguiente función o llamada
            return await call_next(request) #Si no pasa a la siguiente llamada, que ocurra un error...except
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": str(e)})  #se retorna un mensaje de error con jsonresponse y este lo envía como diccionario   
      
    #LISTA CREACIÓN DEL MIDDLEWARE PARA MANEJO DE ERRORES