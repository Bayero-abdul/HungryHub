from flask import request
from flask_restx import Resource, Namespace, fields
from models.cartitem import CartItem
from models.base_model import db

cartitem_ns = Namespace("", description="CRUD operations for cart items")

# Define a cart item model for input and output serialization
cartitem_model = cartitem_ns.model("Cart_Item", {
    "id": fields.Integer(readonly=True),
    "cart_id": fields.Integer(required=True, description="Cart ID"),
    "product_id": fields.Integer(required=True, description="Product ID"),
    "quantity": fields.Integer(required=True, description="Quantity"),
})


#defining cart items CRUD operations
@cartitem_ns.route('/api/cart_items/')
class CartItemsResource(Resource):
    @cartitem_ns.doc(responses={200: 'OK'})
    @cartitem_ns.marshal_list_with(cartitem_model)
    def get(self):
        """Get all cart items"""
        cartitems = CartItem.query.all()
        return cartitems

    @cartitem_ns.doc(responses={201: 'Cart item added', 400: 'Invalid input'})
    @cartitem_ns.marshal_with(cartitem_model, code=201)
    @cartitem_ns.expect(cartitem_model)
    def post(self):
        """Add an item to the cart"""
        data = cartitem_ns.payload
        cartitem = CartItem(
            cart_id=data['cart_id'],
            product_id=data['product_id'],
            quantity=data['quantity']
        )
        db.session.add(cartitem)
        db.session.commit()
        return cartitem, 201

@cartitem_ns.route('/api/cart_items/<int:id>/')
class CartItemResource(Resource):
    @cartitem_ns.doc(responses={200: 'OK', 404: 'Cart item not found'}, params={'id': 'Specify the Cart Item ID'})
    @cartitem_ns.marshal_with(cartitem_model)
    def get(self, id):
        """Get cart item by ID"""
        cartitem = CartItem.query.get_or_404(id)
        return cartitem

    @cartitem_ns.doc(responses={204: 'Cart item removed', 404: 'Cart item not found'}, params={'id': 'Specify the Cart Item ID'})
    def delete(self, id):
        """Remove cart item by ID"""
        cartitem = CartItem.query.get_or_404(id)
        db.session.delete(cartitem)
        db.session.commit()
        return '', 204  
    
    @cartitem_ns.doc(responses={200: 'Cart item updated', 400: 'Invalid input'}, params={'id': 'Specify the Cart Item ID'})
    @cartitem_ns.marshal_with(cartitem_model)
    @cartitem_ns.expect(cartitem_model)
    def put(self, id):
        """Update cart item by ID"""
        cartitem = CartItem.query.get_or_404(id)
        data = cartitem_ns.payload
        cartitem.cart_id = data['cart_id']
        cartitem.product_id = data['product_id']
        cartitem.quantity = data['quantity']
        db.session.commit()
        return cartitem
