from flask import request
from flask_restx import Resource, Namespace, fields
from models.product import Product
from models.ratings import Rating
from models.base_model import db

product_ns = Namespace("", description="CRUD operations for products")

# Define a product model for input and output serialization
product_model = product_ns.model('Product', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'description': fields.String(),
})

product_rating_model = product_ns.model('Rating', {
    'id': fields.Integer(readonly=True),
    'user_id': fields.Integer(required=True),
    'food_id': fields.Integer(required=True),
    'rating': fields.Float(required=True),
})


#defining product CRUD operation
@product_ns.route('/api/products/')
class FoodsListResource(Resource):
    @product_ns.marshal_list_with(product_model)
    def get(self):
        """
        Get all products
        """
        products = Product.query.all()
        return products

    @product_ns.expect(product_model, validate=True)
    @product_ns.marshal_with(product_model, code=201)
    def post(self):
        """
        Create a new product
        """
        data = request.json
        product = Product(**data)
        db.session.add(product)
        db.session.commit()
        return product, 201

@product_ns.route('/api/product/<int:id>/')
class FoodResource(Resource):
    @product_ns.marshal_with(product_model)
    def get(self, id):
        """
        Get product by ID
        """
        product = Product.query.get_or_404(id)
        return product

    @product_ns.expect(product_model, validate=True)
    @product_ns.marshal_with(product_model)
    def put(self, id):
        """
        Update product by ID
        """
        data = request.get_json()
        product = Product.query.get_or_404(id)
        product.name = data['name']
        product.description = data['description']
        db.session.commit()
        return product

    def delete(self, id):
        """
        Delete product by ID
        """
        food = Product.query.get_or_404(id)
        db.session.delete(food)
        db.session.commit()
        return '', 204  

@product_ns.route('/api/product/<int:id>/ratings/')
class FoodRatingsResource(Resource):
    @product_ns.marshal_list_with(product_rating_model)
    def get(self, id):
        """
        Get ratings for a specific product
        """
        ratings = Rating.query.filter_by(food_id=id).all()
        return ratings