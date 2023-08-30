from models.base_model import BaseModel, db

"""
class Users:
    The users class will have a table name called users
    It will have an id of integer type which will be our primary key
    It will have a username of string type
    It will have an email of string type
    It will have a passwd of string type
"""

 
class Users(BaseModel):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True, unique=True,  autoincrement=True)
    username = db.Column(db.String(36), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)


    def __repr__(self):
        """
        The __repr__ method tells python how to print
        object of this class
        which will be useful for debugging
        """
        return f"<User {self.username}>"
