from models.base_model import BaseModel, db



class Orders(BaseModel):
    """
    Represents an order model
    """

    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    is_cancelled = db.Column(db.Boolean, default=False)
    is_fulfilled = db.Column(db.Boolean, default=False)

    # Define a relationship between Order and User
    user = db.relationship('Users', backref='orders')

    # Define a relationship between Order and Cart
    cart = db.relationship('Cart', backref='order')

    def __init__(self, user_id, cart_id):
        self.user_id = user_id
        self.cart_id = cart_id

    def __repr__(self):
        return f"<Order {self.id}>"
