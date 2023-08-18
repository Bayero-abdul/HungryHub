#!/usr/bin/python3
""" Test delete feature
"""
from models.engine.file_storage import FileStorage
from models.restaurant import Restaurant

fs = FileStorage()

# All Restaurants
all_restaurants = fs.all(Restaurant)
print("All Restaurants: {}".format(len(all_restaurants.keys())))
for restaurant_key in all_restaurants.keys():
    print(all_restaurants[restaurant_key])

# Create a new Restaurant
new_restaurant = Restaurant()
new_restaurant.name = "Pepsi"
fs.new(new_restaurant)
fs.save()
print("New Restaurant: {}".format(new_restaurant))

# All Restaurants
all_restaurants = fs.all(Restaurant)
print("All Restaurants: {}".format(len(all_restaurants.keys())))
for restaurant_key in all_restaurants.keys():
    print(all_restaurants[restaurant_key])

# Create another Restaurant
another_restaurant = Restaurant()
another_restaurant.name = "Ribadu"
fs.new(another_restaurant)
fs.save()
print("Another Restaurant: {}".format(another_restaurant))

# All Restaurants
all_restaurants = fs.all(Restaurant)
print("All Restaurants: {}".format(len(all_restaurants.keys())))
for restaurant_key in all_restaurants.keys():
    print(all_restaurants[restaurant_key])        

# Delete the new Restaurant
fs.delete(new_restaurant)

# All Restaurants
all_restaurants = fs.all(Restaurant)
print("All Restaurants: {}".format(len(all_restaurants.keys())))
for restaurant_key in all_restaurants.keys():
    print(all_restaurants[restaurant_key])
