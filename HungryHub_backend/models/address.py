from models.base_model import BaseModel, db



class Address(BaseModel):
    """
    Represents a delivery address in HungryHub app
    """
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    street_address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(100), nullable=False)  

    def __init__(self, user_id, restaurant_id, street_address, city, postal_code, country):
        self.user_id = user_id
        self.restaurant_id = restaurant_id
        self.street_address = street_address
        self.city = city
        self.postal_code = postal_code
        self.country = country  

    def __repr__(self):
        return f"<Address {self.id}: {self.street_address}, {self.city}, {self.postal_code}, {self.country}>"


