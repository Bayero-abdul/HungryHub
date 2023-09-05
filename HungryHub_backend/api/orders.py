from flask import request
from flask_restx import Resource, Namespace, fields
from models.orders import Orders
from models.base_model import db

orders_ns = Namespace("Orders", description="CRUD operations for orders")

# Define an order model for input and output serialization
order_model = orders_ns.model("Order", {
    "id": fields.Integer(readonly=True),
    "user_id": fields.Integer(required=True, description="User ID"),
    "cart_id": fields.Integer(required=True, description="Cart ID"),
    "is_cancelled": fields.Boolean(description="Order cancellation status"),
    "is_fulfilled": fields.Boolean(description="Order fulfillment status")
})


# Define an order item model for input and output serialization
order_item_model = orders_ns.model("OrderItem", {
    "id": fields.Integer(readonly=True),
    "order_id": fields.Integer(required=True, description="Order ID"),
    "food_id": fields.Integer(required=True, description="Food/Product ID"),
    "quantity": fields.Integer(required=True, description="Quantity"),
    "price_per_unit": fields.Float(required=True, description="Price per unit"),
})


# Define an order cancellation model
order_cancellation_model = orders_ns.model("OrderCancellation", {
    "reason": fields.String(required=True, description="Reason for cancellation"),
})


# Define fulfillment model
order_fulfillment_model = orders_ns.model("OrderFulfillment", {
    "fulfillment_status": fields.String(required=True, description="Fulfillment status"),
})




# Implementing orders CRUD operations
@orders_ns.route('/orders/')
class OrdersResource(Resource):
    @orders_ns.doc(responses={200: 'OK'})
    @orders_ns.marshal_list_with(order_model)
    def get(self):
        """Get all orders"""
        orders = Orders.query.all()
        return orders

    @orders_ns.doc(responses={201: 'Order created', 400: 'Invalid input'})
    @orders_ns.marshal_with(order_model, code=201)
    @orders_ns.expect(order_model)
    def post(self):
        """Create a new order"""
        data = orders_ns.payload
        order = Orders(
            user_id=data['user_id'],
            cart_id=data['cart_id']
        )
        db.session.add(order)
        db.session.commit()
        return order, 201

@orders_ns.route('/orders/<int:id>/')
class OrderResource(Resource):
    @orders_ns.doc(responses={200: 'OK', 404: 'Order not found'}, params={'id': 'Specify the Order ID'})
    @orders_ns.marshal_with(order_model)
    def get(self, id):
        """Get order by ID"""
        order = Orders.query.get_or_404(id)
        return order

    @orders_ns.doc(responses={204: 'Order deleted', 404: 'Order not found'}, params={'id': 'Specify the Order ID'})
    def delete(self, id):
        """Delete order by ID"""
        order = Orders.query.get_or_404(id)
        db.session.delete(order)
        db.session.commit()
        return '', 204  # No content response

    @orders_ns.doc(responses={200: 'Order updated', 400: 'Invalid input'}, params={'id': 'Specify the Order ID'})
    @orders_ns.marshal_with(order_model)
    @orders_ns.expect(order_model)
    def put(self, id):
        """Update order by ID"""
        order = Orders.query.get_or_404(id)
        data = orders_ns.payload
        order.user_id = data['user_id']
        order.cart_id = data['cart_id']
        order.is_cancelled = data['is_cancelled']
        order.is_fulfilled = data['is_fulfilled']
        db.session.commit()
        return order


@orders_ns.route('/orders/<int:id>/items/')
class OrderItemsResource(Resource):
    @orders_ns.doc(responses={200: 'OK', 404: 'Order not found'}, params={'id': 'Specify the Order ID'})
    @orders_ns.marshal_list_with(order_item_model)
    def get(self, id):
        """Get items in a specific order"""
        order_items = Orders.query.filter_by(order_id=id).all()
        return order_items
    
# Define a route for order cancellation
@orders_ns.route('/orders/<int:id>/cancel/')
class OrderCancelResource(Resource):
    @orders_ns.doc(responses={200: 'Order cancelled', 400: 'Invalid input'}, params={'id': 'Specify the Order ID'})
    @orders_ns.expect(order_cancellation_model)
    def put(self, id):
        """Cancel a specific order"""
        data = orders_ns.payload

        order = Orders.query.get_or_404(id)
        if order.is_cancelled:
            return {'message': 'Order is already cancelled'}, 400
        order.is_cancelled = True
        order.cancellation_reason = data['reason']

        db.session.commit()
        return {'message': 'Order cancelled'}, 200


# Define a route for order fulfillment
@orders_ns.route('/orders/<int:id>/fulfill/')
class OrderFulfillResource(Resource):
    @orders_ns.doc(responses={200: 'Order fulfilled', 400: 'Invalid input'}, params={'id': 'Specify the Order ID'})
    @orders_ns.expect(order_fulfillment_model)
    def put(self, id):
        """Fulfill a specific order"""
        data = orders_ns.payload

        order = Orders.query.get_or_404(id)
        if order.is_fulfilled:
            return {'message': 'Order is already fulfilled'}, 400
        order.is_fulfilled = True
        order.fulfillment_status = data['fulfillment_status']

        db.session.commit()
        return {'message': 'Order fulfilled'}, 200