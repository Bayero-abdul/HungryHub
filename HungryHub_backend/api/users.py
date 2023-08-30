from flask import request, jsonify
from flask_restx import Resource, Namespace, fields
from models.users import Users
from werkzeug.security import generate_password_hash


user_ns = Namespace("user", description="User CRUD operations")

user_model = user_ns.model(
    "User",
    {
        "id": fields.Integer(required=True, description="User ID"),
        "username": fields.String(required=True, description="Username"),
        "email": fields.String(required=True, description="Email"),
        "password": fields.String(required=True, description="Password")
    }
)

@user_ns.route("/")
class UsersList(Resource):
    @user_ns.doc("list_users")
    @user_ns.marshal_list_with(user_model)
    def get(self):
        """
        Get all users
        """
        users = Users.query.all()
        return users

    @user_ns.doc("create_user")
    @user_ns.expect(user_model)
    @user_ns.marshal_with(user_model, code=201)
    def post(self):
        """
        Create a new user
        """
        data = request.get_json()

        username = data.get('username')
        db_user = Users.query.filter_by(username=username).first()
        if db_user is not None:
            return {"message": f"User with username {username} already exists"}, 400

        new_user = Users(
            username=data.get('username'),
            email=data.get('email'),
            password=generate_password_hash(data.get('password'))
        )

        new_user.save()

        return new_user, 201

@user_ns.route("/<int:id>")
@user_ns.doc(params={"id": "User ID"})
class UserDetail(Resource):
    @user_ns.doc("get_user")
    @user_ns.marshal_with(user_model)
    def get(self, id):
        """
        Get user by ID
        """
        user = Users.query.get(id)
        if user is None:
            return {"message": "User not found"}, 404
        return user

    @user_ns.doc("update_user")
    @user_ns.expect(user_model)
    @user_ns.marshal_with(user_model)
    def put(self, id):
        """
        Update user by ID
        """
        data = request.get_json()
        user = Users.query.get(id)
        if user is None:
            return {"message": "User not found"}, 404
        user.update(
            username=data.get('username'),
            email=data.get('email'),
            password=generate_password_hash(data.get('password'))
        )
        return user

    @user_ns.doc("delete_user")
    def delete(self, id):
        """
        Delete user by ID
        """
        user = Users.query.get(id)
        if user is None:
            return {"message": "User not found"}, 404
        user.delete()
        return {"message": "User deleted successfully"}


