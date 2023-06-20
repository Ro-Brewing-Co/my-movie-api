#Aquí se crea el modelo de las tablas de película
from config.database import Base #Aquí se está importando la variable Base que es la del declarative
from sqlalchemy import Column, Integer, String, Float


class Movie(Base): 
     #Esta va a ser una entidad de mi base de datos
    
    __tablename__ = "movies" #Este será el nombre que tendrá la tabla...

    id = Column(Integer, primary_key = True)
    title = Column(String)
    overview = Column(String)
    year = Column(Integer)                                    #Todo esto es la creación de la tabla de la base de datos
    rating = Column(Float)
    category = Column(String)

    #aHORA ESTO SE PUEDE IMPORTAR EN EL ARCHIVO MAIN.PY
#Esto es lo que aparece en la tabla de sqlite... en el archivo que se genera desde la url de database.py