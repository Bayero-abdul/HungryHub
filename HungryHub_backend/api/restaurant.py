from flask import request, jsonify
from flask_restx import Resource, Namespace, fields
from models.restaurant import Restaurant
from models.product import Product
from models.ratings import Rating
from models.base_model import db



restaurant_ns = Namespace("", description="CRUD operations for restaurants")



# Define the restaurant model for input and output serialization
restaurant_model = restaurant_ns.model("Restaurant", {
    "id": fields.Integer(readonly=True),
    "name": fields.String(required=True, description="Restaurant name"),
    "description": fields.String(description="Restaurant description"),
    "address_id": fields.Integer(required=True, description="ID of the associated address")
})

restauarant_food_model = restaurant_ns.model("Product", {
    "id": fields.Integer(readonly=True),
    "name": fields.String(required=True, description="Product name"),
    "description": fields.String(description="Product description"),
    "restaurant_id": fields.Integer(required=True, description="ID of the associated restaurant")
})

restaurant_rating_model = restaurant_ns.model("Rating", {
    "id": fields.Integer(readonly=True),
    "user_id": fields.Integer(required=True, description="User ID"),
    "restaurant_id": fields.Integer(required=True, description="ID of the associated restaurant"),
    "rating": fields.Float(required=True, description="Rating value")
})




#Implementing CRUD operation for restaurants
@restaurant_ns.route('/api/restaurant/<int:id>/')
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

@restaurant_ns.route('/api/restaurant/')
class RestaurantsResource(Resource):
    @restaurant_ns.doc(responses={200: 'OK'})
    @restaurant_ns.marshal_list_with(restaurant_model)
    def get(self):
        """Get all restaurants"""
        restaurants = Restaurant.query.all()
        return restaurants
    
    
@restaurant_ns.route('/api/restaurant/<int:id>/products/')
class RestaurantFoodsResource(Resource):
    @restaurant_ns.marshal_list_with(restauarant_food_model)
    def get(self, id):
        """Get product offered by a specific restaurant"""
        product = Product.query.filter_by(restaurant_id=id).all()
        return product

@restaurant_ns.route('/api/restaurant/<int:id>/ratings/')
class RestaurantRatingsResource(Resource):
    @restaurant_ns.marshal_list_with(restaurant_rating_model)
    def get(self, id):
        """Get ratings for a specific restaurant"""
        ratings = Rating.query.filter_by(restaurant_id=id).all()
        return ratings

@restaurant_ns.route('/api/restaurants/nearby')
class NearbyRestaurantsResource(Resource):
    @restaurant_ns.doc(params={'lat': 'Latitude', 'lon': 'Longitude'})
    @restaurant_ns.marshal_list_with(restaurant_model)
    def get(self):
        """Get restaurants near a specific location"""
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
        
        # Make a request to the Google Places API
        api_key = 'AIzaSyCze3wuUZ5PlaEy4mT1Go6EGYUsLtDarXE'  # Replaced with my Google API key
        # Set the radius in meters and can be adjusted on need basis
        # searching for restaurants that are located within a 1000-meter radius 
        # or 1 kilometer from the specified latitude and longitude coordinates
        radius = 1000  
        keyword = 'restaurant'  
        google_places_url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lon}&radius={radius}&keyword={keyword}&key={api_key}'
        
        response = request.get(google_places_url)
        
        if response.status_code == 200:
            # Parse the JSON response to extract restaurant information
            data = response.json()
            restaurants = data.get('results', [])
            
            # Map the Google Places API data to your restaurant_model
            nearby_restaurants = []
            for restaurant_data in restaurants:
                name = restaurant_data.get('name', '')
                address = restaurant_data.get('vicinity', '')
                
                # Create a dictionary matching your restaurant_model fields
                restaurant_model_data = {
                    'name': name,
                    'description': '',  
                    'address_id': 0  }
                
                nearby_restaurants.append(restaurant_model_data)
            
            return nearby_restaurants
        else:
            return {'message': 'Unable to retrieve nearby restaurants from Google Places API'}, 500


