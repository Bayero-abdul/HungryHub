#!/usr/bin/python3
from models import storage
from models.base_model import BaseModel
from models.user import User

all_objs = storage.all()
print("-- Reloaded objects --")
for obj_id in all_objs.keys():
    obj = all_objs[obj_id]
    print(obj)

print("-- Create a new User --")
my_user = User()
my_user.first_name = "Betty"
my_user.last_name = "Bar"
my_user.email = "airbnb@mail.com"
my_user.password = "root"
my_user.phone_number = "08108310900"
my_user.role = "admin"
my_user.profile_picture_url = "https://www.google.com/url?sa=i&url=https%3A%2F%2Fpixabay.com%2Fimages%2Fsearch%2Fislamic%2F&psig=AOvVaw2OmN8SKrjyGuuNpQAbDcz1&ust=1691596394892000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCIDXi-S1zYADFQAAAAAdAAAAABAE"

my_user.save()
print(my_user)

print("-- Create a new User 2 --")
my_user2 = User()
my_user2.first_name = "John"
my_user2.last_name = "obi"
my_user2.email = "air2@mail.com"
my_user2.password = "root"
my_user2.phone_number = "08145324513"
my_user2.role = "user"
my_user2.profile_picture_url = "https://www.google.com/url?sa=i&url=https%3A%2F%2Fpixabay.com%2Fimages%2Fsearch%2Fislamic%2F&psig=AOvVaw2OmN8SKrjyGuuNpQAbDcz1&ust=1691596394892000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCIDXi-S1zYADFQAAAAAdAAAAABAE"
my_user2.save()
print(my_user2)
