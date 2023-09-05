from models.base_model import BaseModel, db
from models.users import Users  
from models.orders import Orders 




class Payment(BaseModel):
    """
    Represents a payment model
    """

    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(50), nullable=False)

    # Define a relationship between Payment and User
    user = db.relationship('User', backref='payments')

    # Define a relationship between Payment and Order
    order = db.relationship('Order', backref='payments')

    def __init__(self, user_id, order_id, amount, payment_status):
        self.user_id = user_id
        self.order_id = order_id
        self.amount = amount
        self.payment_status = payment_status

    def __repr__(self):
        return f"<Payment {self.id}>"
