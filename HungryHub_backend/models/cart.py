from models.base_model import BaseModel, db


class Cart(BaseModel):
    """
    Represents a cart model
    """

    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_checked_out = db.Column(db.Boolean, default=False)

    # Define a relationship between Cart and User
    user = db.relationship('User', backref='carts')

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return f"<Cart {self.id}>"
