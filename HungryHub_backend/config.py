
from decouple import config
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Config:
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS', cast=bool)
   
   
class DatabaseConfig:
    """
    Retrieve the value of 'DATABASE_URI' from the .env file using the 'config' function
    This variable will hold the URI for connecting to the database
    """ 
    DATABASE_URI = config('DATABASE_URI')
    

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = DatabaseConfig.DATABASE_URI
    DEBUG = config('DEBUG', cast=bool)
    #enable us to see SQL statement generated by SQLALCHEMY in the console log
    SQLALCHEMY_ECHO = True 

class ProdConfig(Config):
    pass

class TestConfig(Config):
    pass
