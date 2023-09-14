from flask import request
from flask_restx import Resource, Namespace, fields
from models.cart import Cart
from models.cartitem import CartItem
from models.orders import Orders
from models.base_model import db

cart_ns = Namespace("", description="CRUD operations for carts")

# Define a cart model for input and output serialization
cart_model = cart_ns.model("Cart", {
    "id": fields.Integer(readonly=True),
    "user_id": fields.Integer(required=True, description="User ID"),
    "is_checked_out": fields.Boolean(description="Cart checkout status")
})

# Define a cart item model for input and output serialization
cart_item_model = cart_ns.model("CartItem", {
    "id": fields.Integer(readonly=True),
    "cart_id": fields.Integer(required=True, description="Cart ID"),
    "product_id": fields.Integer(required=True, description="Product ID"),
    "quantity": fields.Integer(required=True, description="Quantity"),
    "price": fields.Float(required=True, description="Price per unit"),
})

# Define a checkout model for input and output serialization
checkout_model = cart_ns.model("Checkout", {
    "cart_id": fields.Integer(required=True, description="Cart ID"),
    "total_price": fields.Float(required=True, description="Total price"),
    "payment_method": fields.String(required=True, description="Payment method"),
})


#defining cart CRUD operation
@cart_ns.route('/api/carts/')
class CartsResource(Resource):
    @cart_ns.doc(responses={200: 'OK'})
    @cart_ns.marshal_list_with(cart_model)
    def get(self):
        """Get all carts"""
        carts = Cart.query.all()
        return carts

    @cart_ns.doc(responses={201: 'Cart created', 400: 'Invalid input'})
    @cart_ns.marshal_with(cart_model, code=201)
    @cart_ns.expect(cart_model)
    def post(self):
        """Create a new cart"""
        data = cart_ns.payload
        cart = Cart(user_id=data['user_id'])
        db.session.add(cart)
        db.session.commit()
        return cart, 201

@cart_ns.route('/api/carts/<int:id>/')
class CartResource(Resource):
    @cart_ns.doc(responses={200: 'OK', 404: 'Cart not found'}, params={'id': 'Specify the Cart ID'})
    @cart_ns.marshal_with(cart_model)
    def get(self, id):
        """Get cart by ID"""
        cart = Cart.query.get_or_404(id)
        return cart

    @cart_ns.doc(responses={204: 'Cart deleted', 404: 'Cart not found'}, params={'id': 'Specify the Cart ID'})
    def delete(self, id):
        """Delete cart by ID"""
        cart = Cart.query.get_or_404(id)
        db.session.delete(cart)
        db.session.commit()
        return '', 204

    @cart_ns.doc(responses={200: 'Cart updated', 400: 'Invalid input'}, params={'id': 'Specify the Cart ID'})
    @cart_ns.marshal_with(cart_model)
    @cart_ns.expect(cart_model)
    def put(self, id):
        """Update cart by ID"""
        cart = Cart.query.get_or_404(id)
        data = cart_ns.payload
        cart.user_id = data['user_id']
        cart.is_checked_out = data['is_checked_out']
        db.session.commit()
        return cart


@cart_ns.route('/api/carts/<int:id>/items/')
class CartItemsResource(Resource):
    @cart_ns.doc(responses={200: 'OK', 404: 'Cart not found'}, params={'id': 'Specify the Cart ID'})
    @cart_ns.marshal_list_with(cart_item_model)
    def get(self, id):
        """Get items in a specific cart"""
        cart_items = CartItem.query.filter_by(cart_id=id).all()
        return cart_items

    @cart_ns.doc(responses={201: 'Cart item added', 400: 'Invalid input'}, params={'id': 'Specify the Cart ID'})
    @cart_ns.marshal_with(cart_item_model, code=201)
    @cart_ns.expect(cart_item_model)
    def post(self, id):
        """Add an item to a specific cart"""
        data = cart_ns.payload
        cart_item = CartItem(
            cart_id=id,
            product_id=data['product_id'],
            quantity=data['quantity'],
            price=data['price']
        )
        db.session.add(cart_item)
        db.session.commit()
        return cart_item, 201


# Define a function to calculate the total price of items in the cart
def calculate_total_price(cart):
    total_price = 0.0
    cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
    for cart_item in cart_items:
        total_price += cart_item.quantity * cart_item.price
    return total_price

# Define a function to create an order
def create_order(cart, total_price, payment_method):
    order = Orders(
        user_id=cart.user_id,
        total_price=total_price,
        payment_method=payment_method,
    )
    db.session.add(order)
    
    cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
    for cart_item in cart_items:
        cart_item.order_id = order.id

    db.session.commit()
    return order


# Implementing the checkout logic 
@cart_ns.route('/api/carts/<int:id>/checkout/')
class CartCheckoutResource(Resource):
    @cart_ns.doc(responses={200: 'Checkout successful', 400: 'Invalid input'}, params={'id': 'Specify the Cart ID'})
    @cart_ns.expect(checkout_model)
    def post(self, id):
        """Checkout a cart and create an order"""
        data = cart_ns.payload
        cart = Cart.query.get_or_404(id)

        if cart.is_checked_out:
            return {'message': 'Cart has already been checked out'}, 400

        total_price = calculate_total_price(cart)
        order = create_order(cart, total_price, data['payment_method'])
        cart.is_checked_out = True
        db.session.commit()
        
        return {'message': 'Checkout successful', 'order_id': order.id}, 200