from flask import request, jsonify
from flask_restx import Resource, Namespace, fields
from models.restaurant import Restaurant
from models.base_model import db



restaurant_ns = Namespace("restaurant", description="CRUD operations for restaurants")



# Define the restaurant model for input and output serialization
restaurant_model = restaurant_ns.model("Restaurant", {
    "id": fields.Integer(readonly=True),
    "name": fields.String(required=True, description="Restaurant name"),
    "description": fields.String(description="Restaurant description"),
    "address_id": fields.Integer(required=True, description="ID of the associated address")
})




@restaurant_ns.route('/<int:id>')
class RestaurantResource(Resource):
    @restaurant_ns.doc(responses={200: 'OK', 404: 'Restaurant not found'}, params={'id': 'Specify the Restaurant ID'})
    @restaurant_ns.marshal_with(restaurant_model)
    def get(self, id):
        """Get a restaurant by ID"""
        restaurant = Restaurant.query.get(id)
        if restaurant:
            return restaurant 
        else:
            return {'message': 'Restaurant not found'}, 404
        

    @restaurant_ns.doc(responses={201: 'Restaurant created', 400: 'Invalid input'})
    @restaurant_ns.marshal_with(restaurant_model)
    @restaurant_ns.expect(restaurant_model)
    def post(self):
        """Create a new restaurant"""
        data = restaurant_ns.payload
        restaurant = Restaurant(
            name=data['name'], 
            description=data.get('description'), 
            address_id=data['address_id'])
        db.session.add(restaurant)
        db.session.commit()
        return {'message': 'Restaurant created', 'id': restaurant.id}, 201

    @restaurant_ns.doc(responses={204: 'Restaurant deleted', 404: 'Restaurant not found'})
    @restaurant_ns.marshal_with(restaurant_model)
    def delete(self, id):
        """Delete a restaurant by ID"""
        restaurant = Restaurant.query.get(id)
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return {'message': 'Restaurant deleted'}, 204
        else:
            return {'message': 'Restaurant not found'}, 404

    @restaurant_ns.doc(responses={200: 'Restaurant updated', 400: 'Invalid input'}, params={'id': 'Specify the Restaurant ID'})
    @restaurant_ns.marshal_with(restaurant_model)
    @restaurant_ns.expect(restaurant_model)
    def put(self, id):
        """Update a restaurant by ID"""
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {'message': 'Restaurant not found'}, 404

        data = restaurant_ns.payload
        restaurant.name = data['name']
        restaurant.description = data.get('description')
        restaurant.address_id = data['address_id']
        db.session.commit()
        return {'message': 'Restaurant updated'}, 200

@restaurant_ns.route('/')
class RestaurantsResource(Resource):
    @restaurant_ns.doc(responses={200: 'OK'})
    @restaurant_ns.marshal_list_with(restaurant_model)
    def get(self):
        """Get all restaurants"""
        restaurants = Restaurant.query.all()
        return restaurants
