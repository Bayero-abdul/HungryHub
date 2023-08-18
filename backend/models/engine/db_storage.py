#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.base_model import BaseModel, Base
from models.user import User
from models.restaurant import Restaurant
from models.address import Address
from models.order import Order
from models.cart import Cart
from models.cart import CartItem
from models.food import Food
from models.payment import Payment
from models.rating import Rating
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {'User': User,
           'Restaurant': Restaurant,
           'Address': Address,
           'Food': Food,
           'Order': Order,
           'Cart': Cart,
           'CartItem': CartItem,
           'Payment': Payment,
           'Rating': Rating
           }


class DBStorage:
    """interacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        HUB_MYSQL_USER = getenv('HUB_MYSQL_USER')
        HUB_MYSQL_PWD = getenv('HUB_MYSQL_PWD')
        HUB_MYSQL_HOST = getenv('HUB_MYSQL_HOST')
        HUB_MYSQL_DB = getenv('HUB_MYSQL_DB')
        HUB_ENV = getenv('HUB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HUB_MYSQL_USER,
                                             HUB_MYSQL_PWD,
                                             HUB_MYSQL_HOST,
                                             HUB_MYSQL_DB))
        if HUB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    """def all(self, cls=None):
        query on the current database session
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)"""

    def all(self, cls=None):
        '''Retrieves all instances of an optional provided class name from the
            current database session'''
        all_objs = {}
        if cls is None:
            for c in classes.values():
                q = self.__session.query(c)
                for o in q:
                    k = o.to_dict()['__class__'] + '.' + o.id
                    if '_sa_instance_state' in o.__dict__:
                        del o.__dict__['_sa_instance_state']
                    all_objs[k] = o
            return all_objs
        cls = eval(cls) if type(cls) is str else cls
        if cls in classes.values():
            q = self.__session.query(cls)
            for o in q:
                k = o.to_dict()['__class__'] + '.' + o.id
                all_objs[k] = o
            return all_objs
        else:
            return None

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count
