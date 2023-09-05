from models.base_model import BaseModel, db

class Product(BaseModel):
    """
    Represents a product model
    """

    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<Food {self.id}: {self.name}>"
