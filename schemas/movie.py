from pydantic import BaseModel, Field
from typing import Optional #Esto para dar opcion en la clase Movie el id la requiere. La clase List es para generar respuestas en listas.

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