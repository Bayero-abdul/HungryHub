from flask import request
from flask_restx import Resource, Namespace, fields
from models.payment import Payment
from models.base_model import db

payment_ns = Namespace("", description="CRUD operations for payment")

# Define a payment model for input and output serialization
payment_model = payment_ns.model('Payment', {
    'id': fields.Integer(readonly=True),
    'user_id': fields.Integer(required=True),
    'order_id': fields.Integer(required=True),
    'amount': fields.Float(required=True),
    'payment_status': fields.String(required=True),
})


#defining CRUD operations for payment
@payment_ns.route('/api/payments/')
class PaymentsListResource(Resource):
    @payment_ns.marshal_list_with(payment_model)
    def get(self):
        """
        Get all payments
        """
        payments = Payment.query.all()
        return payments

    @payment_ns.expect(payment_model, validate=True)
    @payment_ns.marshal_with(payment_model, code=201)
    def post(self):
        """
        Create a new payment
        """
        data = request.get_json()
        payment = Payment(**data)
        db.session.add(payment)
        db.session.commit()
        return payment, 201

@payment_ns.route('/api/payment/<int:id>')
class PaymentResource(Resource):
    @payment_ns.marshal_with(payment_model)
    def get(self, id):
        """
        Get payment by ID
        """
        payment = Payment.query.get_or_404(id)
        return payment

    @payment_ns.expect(payment_model, validate=True)
    @payment_ns.marshal_with(payment_model)
    def put(self, id):
        """
        Update payment by ID
        """
        data = request.json
        payment = Payment.query.get_or_404(id)
        payment.user_id = data['user_id']
        payment.order_id = data['order_id']
        payment.amount = data['amount']
        payment.payment_status = data['payment_status']
        db.session.commit()
        return payment

    def delete(self, id):
        """
        Delete payment by ID
        """
        payment = Payment.query.get_or_404(id)
        db.session.delete(payment)
        db.session.commit()
        return '', 204 

