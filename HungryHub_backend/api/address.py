from flask import request, jsonify
from flask_restx import Resource, Namespace, fields
from models.address import Address  
from models.base_model import db




address_ns = Namespace("Address", description="CRUD operations for addresses")

# Define a model for serialization/deserialization
address_model = address_ns.model("Address", {
    'id': fields.Integer(readOnly=True, description='The unique identifier of an address'),
    'user_id': fields.Integer(required=True, description='The ID of the user associated with the address'),
    'restaurant_id': fields.Integer(required=True, description='The ID of the restaurant associated with the address'),
    'street_address': fields.String(required=True, description='The street address'),
    'city': fields.String(required=True, description='The city'),
    'postal_code': fields.String(required=True, description='The postal code'),
    'country': fields.String(required=True, description='The country'),
})

#define CRUD operations for address endpoint
@address_ns.route('/address/<int:id>')
@address_ns.param('id', 'The unique identifier of an address')
class AddressResource(Resource):
    @address_ns.marshal_with(address_model)
    def get(self, id):
        """
        Get a single address by ID
        """
        address = Address.query.get(id)
        if address:
            return address, 200
        else:
            return {'message': 'Address not found'}, 404

    @address_ns.expect(address_model)
    @address_ns.marshal_with(address_model)
    def put(self, id):
        """
        Update an address by ID
        """
        address = Address.query.get(id)
        if not address:
            return {'message': 'Address not found'}, 404

        # Update the address fields based on the request data
        data = request.json
        address.user_id = data['user_id']
        address.restaurant_id = data['restaurant_id']
        address.street_address = data['street_address']
        address.city = data['city']
        address.postal_code = data['postal_code']
        address.country = data['country']

        db.session.commit()
        return address, 200

    def delete(self, id):
        """
        Delete an address by ID
        """
        address = Address.query.get(id)
        if not address:
            return {'message': 'Address not found'}, 404

        db.session.delete(address)
        db.session.commit()
        return {'message': 'Address deleted'}, 204

@address_ns.route('/address/')
class AddressListResource(Resource):
    @address_ns.marshal_list_with(address_model)
    def get(self):
        """
        Get a list of all addresses
        """
        addresses = Address.query.all()
        return addresses, 200

    @address_ns.expect(address_model)
    @address_ns.marshal_with(address_model, code=201)
    def post(self):
        """
        Create a new address
        """
        data = request.json
        address = Address(
            user_id=data['user_id'],
            restaurant_id=data['restaurant_id'],
            street_address=data['street_address'],
            city=data['city'],
            postal_code=data['postal_code'],
            country=data['country']
        )

        db.session.add(address)
        db.session.commit()
        return address, 201







