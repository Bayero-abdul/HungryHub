#!/usr/bin/python3
from flask import Flask
from flask_restx import Api
from models.users import Users, db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from api.authentication import auth
from api.users import user_ns
from api.address import address_ns
from api.restaurant import restaurant_ns
from api.payment import payment_ns
from api.product import product_ns
from api.cart import cart_ns
from api.cartitem import cartitem_ns
from api.orders import orders_ns
from api.ratings import ratings_ns
from models.address import Address
from models.payment import Payment
from models.restaurant import Restaurant
from models.cartitem import CartItem
from models.cart import Cart
from models.orders import Orders
from models.ratings import Rating
from models.product import Product

app = Flask(__name__)

# Load configuration
app.config.from_object("config.DevelopmentConfig")

# Initialize the app with the extension
db.init_app(app)


#This code configures CORS to allow requests from  http://localhost:3000 
#to any route matching /api/* on the Flask server.
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Initialize migration
migrate = Migrate(app, db)

# Initialize JWTManager
JWTManager(app)

# Initialize API
api = Api(app, doc='/swagger', description="Api Endpoints")

api.add_namespace(auth)
api.add_namespace(user_ns)
api.add_namespace(address_ns)
api.add_namespace(restaurant_ns)
api.add_namespace(payment_ns)
api.add_namespace(product_ns)
api.add_namespace(cart_ns)
api.add_namespace(cartitem_ns)
api.add_namespace(orders_ns)
api.add_namespace(ratings_ns)


@app.shell_context_processor
def shell():
    return {
        "database": db,
        "User": Users,
        "Address": Address,
        "Restaurant": Restaurant,
        "Payments": Payment,
        "Cart_items": CartItem,
        "Cart": Cart,
        "Order": Orders,
        "Ratings": Rating,
        "Product": Product,   
    }



if __name__ == "__main__":
    app.run()
