import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker #Esto es para crear la sesion
from sqlalchemy.ext.declarative import declarative_base #Esto sirve para manipular todas las tablas de la base de datos

sqlite_file_name = "../database.sqlite" #Aquí se guarda el nombre de la base de datos... ../ es para que la tabla de la base de datos se genere en la carpeta principal
base_dir = os.path.dirname(os.path.realpath(__file__)) #Esto lee el directorio actual de el archivo database.py

database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"                       #Las tres barras es la forma de conectarse a una base de datos
                                                                #el método join se utiliza para unir las uls que se tiene(sqlite_file_name y base_dir) 

engine  =    create_engine(database_url, echo=True)                #Esto representa el motor de la base de datos   de sqalchemy es debido importa el método create_engine                                             
#aL Create_engine se le pasa como parámetro la url que es database_url...echo es para que al momento de crear la base de datos 
#poder visualizar el código en consola
Session = sessionmaker(bind=engine)#Se debe crear una session para conectarse a la base de datos, es igual a una función importada sqalchemy
#El parámetro bind es para enlazarse al motor de la base de datos que es engine

Base = declarative_base() #Sirve para manejo de tablas en la base de datos 
