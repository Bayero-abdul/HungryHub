from models.base_model import BaseModel, db
  

class Rating(BaseModel):
    """
    Represents a rating model
    """

    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)  # Corrected table name
    rating = db.Column(db.Float, nullable=False)

    # Define a relationship between Rating and User
    user = db.relationship('User', backref='ratings')

    # Define a relationship between Rating and Product
    product = db.relationship('Product', backref='ratings')  # Corrected relationship name

    def __init__(self, user_id, product_id, rating):
        self.user_id = user_id
        self.product_id = product_id
        self.rating = rating

    def __repr__(self):
        return f"<Rating {self.id}>"
