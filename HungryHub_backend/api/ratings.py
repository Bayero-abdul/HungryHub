from flask import request
from flask_restx import Resource, Namespace, fields
from models.ratings import Rating
from models.product import Product
from models.base_model import db
from sqlalchemy import func

ratings_ns = Namespace("Ratings", description="CRUD operations for ratings")

# Define a rating model for input and output serialization
rating_model = ratings_ns.model("Rating", {
    "id": fields.Integer(readonly=True),
    "user_id": fields.Integer(required=True, description="User ID"),
    "product_id": fields.Integer(required=True, description="Product ID"),
    "rating": fields.Float(required=True, description="Rating value"),
})


# Implementing ratings CRUD operations
@ratings_ns.route('/ratings/')
class RatingsResource(Resource):
    @ratings_ns.doc(responses={200: 'OK'})
    @ratings_ns.marshal_list_with(rating_model)
    def get(self):
        """Get all ratings"""
        ratings = Rating.query.all()
        return ratings

    @ratings_ns.doc(responses={201: 'Rating added', 400: 'Invalid input'})
    @ratings_ns.marshal_with(rating_model, code=201)
    @ratings_ns.expect(rating_model)
    def post(self):
        """Add a new rating"""
        data = ratings_ns.payload
        rating = Rating(
            user_id=data['user_id'],
            food_id=data['food_id'],
            rating=data['rating']
        )
        db.session.add(rating)
        db.session.commit()
        return rating, 201

@ratings_ns.route('/ratings/<int:id>/')
class RatingResource(Resource):
    @ratings_ns.doc(responses={200: 'OK', 404: 'Rating not found'}, params={'id': 'Specify the Rating ID'})
    @ratings_ns.marshal_with(rating_model)
    def get(self, id):
        """Get rating by ID"""
        rating = Rating.query.get_or_404(id)
        return rating

    @ratings_ns.doc(responses={204: 'Rating deleted', 404: 'Rating not found'}, params={'id': 'Specify the Rating ID'})
    def delete(self, id):
        """Delete rating by ID"""
        rating = Rating.query.get_or_404(id)
        db.session.delete(rating)
        db.session.commit()
        return '', 204  
    
    @ratings_ns.doc(responses={200: 'Rating updated', 400: 'Invalid input'}, params={'id': 'Specify the Rating ID'})
    @ratings_ns.marshal_with(rating_model)
    @ratings_ns.expect(rating_model)
    def put(self, id):
        """Update rating by ID"""
        rating = Rating.query.get_or_404(id)
        data = ratings_ns.payload
        rating.user_id = data['user_id']
        rating.food_id = data['food_id']
        rating.rating = data['rating']
        db.session.commit()
        return rating


@ratings_ns.route('/ratings/avg/<int:product_id>/')
class AverageRatingResource(Resource):
    @ratings_ns.doc(responses={200: 'OK', 404: 'Product not found'}, params={'product_id': 'Specify the Product ID'})
    def get(self, product_id):
        """Get the average rating for a specific product"""
        
        # First, check if the specified product_id exists
        product = Product.query.get(product_id)
        if not product:
            return {'message': 'Product not found'}, 404
        
        # Calculate the average rating using SQLAlchemy's aggregation functions
        avg_rating = db.session.query(func.avg(Rating.rating)).filter_by(product_id=product_id).scalar()
        
        # Return the result, you can round the average rating to a specific number of decimal places
        return {'average_rating': round(avg_rating, 2)}  # Here it has been Rounded to 2 decimal places
