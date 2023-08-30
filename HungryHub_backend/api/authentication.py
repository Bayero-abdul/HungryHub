from flask import request, jsonify
from flask_restx import Resource, Namespace, fields
from models.users import Users
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from api.users import user_ns 


auth = Namespace("auth", description = "user authentication")





"""
defining serializtion schema for models
serialization is where data types such as object or data structures
are converted into formats that can easily be transmited or stored
in formats such as JSON
"""
#This is sign up model
signup_model = auth.model(
    "Signup", {
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "password":fields.String(required=True)
    }
)

#This is login model
login_model = auth.model(
    "login", {
        "username": fields.String(required=True),
        "password": fields.String(required=True)
    }
)






@auth.route("/signup")
class Signup(Resource):
    @auth.marshal_with(signup_model)
    @auth.expect(signup_model)
    def post(self):#this ia POST HTTP request
        data = request.get_json()

        username = data.get('username')
        db_user = Users.query.filter_by(username=username).first()
        if db_user is not None:
            return jsonify({"message": f"User with username {username} already exists"})

        new_user = Users(
            username = data.get('username'),
            email = data.get('email'),
            password = generate_password_hash(data.get('password'))
        )

        new_user.save()

        return jsonify({"message": "User created Successfully"})
    


    
@auth.route("/login")
class Login(Resource):
    @auth.expect(login_model)
    def post(self):
        data = request.get_json() #api.payload is used in accessing parsed JSON data

        username = data.get('username')
        password = data.get('password')

        db_user = Users.query.filter_by(username=username).first()

        if db_user and check_password_hash(db_user.password, password):
            access_token = create_access_token(identity=db_user.username)
            refresh_token = create_refresh_token(identity=db_user.username)

            return jsonify({
                "access_token": access_token,
                "refresh_token": refresh_token
                })
    
