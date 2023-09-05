from models.base_model import BaseModel, db


class CartItem(BaseModel):
    """
    Represents items within a cart
    """

    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    # Define a relationship between CartItem and Products
    product = db.relationship('Product', backref='cart_items')

    def __init__(self, cart_id, product_id, quantity):
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity

    def __repr__(self):
        return f"<CartItem {self.id}>"
