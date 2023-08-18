import unittest
import os
import hashlib
from models.base_model import BaseModel
from models.user import User

class TestUser(unittest.TestCase):

    def test_unique_id(self):
        """Test for id uniqueness"""
        user1 = User()
        user2 = User()

        self.assertTrue(user1.id != user2.id)
        self.assertFalse(user1.id == user2.id)
 
    def test_create_user(self):
        """test if User Class works correctly"""
        user_data = {
            "email": "test@example.com",
            "password": "password123",
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "123-456-7890",
            "role": "user",
            "profile_picture_url": "https://example.com/profile.jpg"
        }
        
        user = User(**user_data)

        self.assertEqual(user.email, user_data["email"])
        self.assertEqual(user.password, user_data["password"])
        self.assertEqual(user.first_name, user_data["first_name"])
        self.assertEqual(user.last_name, user_data["last_name"])
        self.assertEqual(user.phone_number, user_data["phone_number"])
        self.assertEqual(user.role, user_data["role"])
        self.assertEqual(
            user.profile_picture_url,
            user_data["profile_picture_url"])

    def test_default_values(self):
        user = User()
        self.assertEqual(user.email, "")
        self.assertEqual(user.password, "")
        self.assertEqual(user.first_name, "")
        self.assertEqual(user.last_name, "")
        self.assertEqual(user.phone_number, "")
        self.assertEqual(user.role, "")
        self.assertEqual(user.profile_picture_url, "")

    def test_set_attributes(self):
        user = User()
        user.email = "test@example.com"
        user.password = "password123"
        user.first_name = "John"
        user.last_name = "Doe"
        user.phone_number = "123-456-7890"
        user.role = "user"
        user.profile_picture_url = "https://example.com/profile.jpg"


        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.password, "password123")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.phone_number, "123-456-7890")
        self.assertEqual(user.role, "user")
        self.assertEqual(
            user.profile_picture_url,
            "https://example.com/profile.jpg")

    def test__str__(self):
        """Test for the string representation."""
        user = User()
        self.assertEqual(str(user), "[User] ({}) {}"
                         .format(user.id, user.__dict__))


    def test_serialization_and_deserialization(self):
        user_data = {
            "email": "test@example.com",
            "password": "password123",
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "123-456-7890",
            "role": "user",
            "profile_picture_url": "https://example.com/profile.jpg"
        }

        user = User(**user_data)

        # Serialize user to dictionary
        user_dict = user.to_dict()
        self.assertTrue(isinstance(user_dict, dict))
        self.assertEqual(user_dict['__class__'], 'User')
        self.assertEqual(user_dict['email'], user_data['email'])
        self.assertEqual(user_dict['password'], user_data['password'])
        self.assertEqual(user_dict['created_at'], user.created_at.isoformat())
        self.assertEqual(user_dict['updated_at'], user.updated_at.isoformat())

        # Deserialize dictionary to user object
        deserialized_user = User(**user_dict)
        self.assertEqual(deserialized_user.email, user.email)
        self.assertEqual(deserialized_user.password, user.password)
        self.assertEqual(deserialized_user.created_at, user.created_at)
        self.assertEqual(deserialized_user.updated_at, user.updated_at)

    def test_inherited_attributes(self):
        user = User()
        self.assertTrue(hasattr(user, 'id'))
        self.assertTrue(hasattr(user, 'created_at'))
        self.assertTrue(hasattr(user, 'updated_at'))

    def test_inherited_methods(self):
        user = User()

        # Test __str__ method inherited from BaseModel
        self.assertIsInstance(user.__str__(), str)

        # Test to_dict method inherited from BaseModel
        user_dict = user.to_dict()
        self.assertTrue(isinstance(user_dict, dict))
        self.assertEqual(user_dict['email'], user.email)
        self.assertEqual(user_dict['password'], user.password)

    def test_save_method(self):
        user = User()
        initial_updated_at = user.updated_at
        user.save()
        self.assertNotEqual(initial_updated_at, user.updated_at)

    def test_to_dict_method(self):
        user_data = {
            "email": "test@example.com",
            "password": "password123",
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "123-456-7890",
            "role": "user",
            "profile_picture_url": "https://example.com/profile.jpg"
        }

        user = User(**user_data)
        user_dict = user.to_dict()

        self.assertTrue(isinstance(user_dict, dict))
        self.assertEqual(user_dict['__class__'], 'User')
        self.assertEqual(user_dict['email'], user_data['email'])
        self.assertEqual(user_dict['password'], user_data['password'])
        self.assertEqual(user_dict['created_at'], user.created_at.isoformat())
        self.assertEqual(user_dict['updated_at'], user.updated_at.isoformat())
	
    def test_to_dict_has_class_attr(self):
        """Test if to_dict() has __class__ attribute."""
        user = User()
        user_json = user.to_dict()
        self.assertTrue(hasattr(user_json, '__class__'))
    

if __name__ == '__main__':
    unittest.main()
