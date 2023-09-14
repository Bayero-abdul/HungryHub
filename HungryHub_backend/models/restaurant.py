from models.base_model import BaseModel, db



class Restaurant(BaseModel):
    """
    Represents a restaurant model
    """

    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(157), nullable=False)
    description = db.Column(db.Text)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=False)

     # Define a relationship between Restaurant and Address
    address = db.relationship('Address', backref='restaurant', foreign_keys=[address_id])

    def __init__(self, name, description, address_id):
        self.name = name
        self.description = description
        self.address_id = address_id

    def __repr__(self):
        return f"<Restaurant {self.id}: {self.name}>"
