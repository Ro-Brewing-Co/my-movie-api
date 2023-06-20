from jwt import encode, decode #Importtamos esta clase para crear el token... para validar el token se usa decode con los parámetros decode(token, key="my_secret_key", algoriyhms=["HS256"])

def create_token(data: dict):  #Esta función crea el token con parámetro que es un diccionario con informaci´pno que se convierte al token.
    token: str = encode(payload=data, key="my_secret_key", algorithm="HS256")  
    return token
     #payload es el contenido que se va a convertir al token, en este caso es data.El token también tiene una clave secreta (key)
     #El algoritmo es algo que debe llevar el token y elste código lo recomienda
     #Se crea como variable de tipo str
     #Luego se debe ir al archivo main para importar esta función creada aquí.

def validate_token(token: str) -> dict:
    data: dict = decode(token, key="my_secret_key", algorithms=["HS256"])
    return data