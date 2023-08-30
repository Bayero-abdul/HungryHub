#!/usr/bin/python3
from flask import Flask
from flask_restx import Api
from models.users import Users, db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from api.authentication import auth
from api.users import user_ns
from api.address import address_ns
from api.restaurant import restaurant_ns
from models.address import Address
from models.restaurant import Restaurant




def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    # initialize the app with the extension
    db.init_app(app)
    

    # Initialize migration
    migrate = Migrate(app, db)
    # Initialize JWTManager
    JWTManager(app)
    # Initialize API
    api = Api(app, doc='/docs')
    
    api.add_namespace(auth)
    api.add_namespace(user_ns)
    api.add_namespace(address_ns)
    api.add_namespace(restaurant_ns)







    @app.shell_context_processor
    def shell():
        return {
            "database": db,
            "User": Users,
            "Address": Address,
            "Restaurant": Restaurant
            }


    return app












"""
def main():
    #we can use this function to create database tables
    # based on the defined models
    #but in our case we set FLASK_APP environmental variable to the name 
    #of our python script which is app.py
    #to serves as the entry point for our Flask application
    #after which we accessed flask shell and run db.create_all()
    db.create_all()
"""