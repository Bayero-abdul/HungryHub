from flask_sqlalchemy import SQLAlchemy



#i have not specified it to app because I want it to be a global variable
#which i can access within other parts of our directory containing all my codes
db = SQLAlchemy()


class BaseModel(db.Model):
    """
    Base model for common CRUD (Create, Read, Update, Delete) operations.

    This class provides basic methods for interacting with a database using SQLAlchemy.

    Attributes:
        __abstract__ (bool): Indicates that this class is not meant to be instantiated directly.

    Methods:
        save(): Save the current instance to the database.
        delete(): Delete the current instance from the database.
        update(**kwargs): Update the attributes of the current instance with new values.

    """
    __abstract__ = True

    def save(self):
        """
        Save the current instance to the database.

        This method adds the current instance to the current database session
        and commits the transaction to persist the changes to the database.

        Returns:
            bool: True if the save operation was successful, False if there was an error.

        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Delete the current instance from the database.

        This method marks the current instance for deletion in the current
        database session and commits the transaction to remove it from the database.

        Returns:
            bool: True if the delete operation was successful, False if there was an error.

        """
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        """
        Update the attributes of the current instance with new values.

        This method accepts keyword arguments where each keyword represents
        an attribute to update, and its associated value is the new value.

        Args:
            **kwargs: Keyword arguments where the key is the name of the attribute
                to update, and the value is the new value.

        Returns:
            bool: True if the update operation was successful, False if there was an error.

        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
