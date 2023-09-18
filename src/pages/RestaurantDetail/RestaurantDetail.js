import React, { useState, useEffect } from "react";
import axios from "axios";
import "./RestaurantDetail.css";

const BASE_URL = "http://127.0.0.1:5000";

function RestaurantDetail({ restaurantId }) {
  const [restaurant, setRestaurant] = useState(null);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  // Dummy Data
  const dummyRestaurant = {
    name: "Dummy Restaurant",
    backgroundImage:
      "https://img.freepik.com/free-photo/big-sandwich-hamburger-with-juicy-beef-burger-cheese-tomato-red-onion-wooden-table_2829-19631.jpg?w=2000&t=st=1693151783~exp=1693152383~hmac=5392722df03d607c86ebc98dd07aa7e3e5c43fefe11ad7cae9d67f4997fed506", // Adjust the path to your dummy image
  };

  const dummyProducts = [
    {
      id: 1,
      name: "Dummy Food 1",
      description: "This is a dummy food description",
      backgroundImage:
        "https://img.freepik.com/free-photo/tasty-beef-burger-ready-be-served_23-2148290587.jpg?w=1060&t=st=1695017405~exp=1695018005~hmac=7413418e9bf58927d19fc7c48b768373101d9572c69bff79857ed966a7a0f1ac",
      price: 12.99,
    },
    {
      id: 2,
      name: "Dummy Food 2",
      description: "This is dummy food description",
      backgroundImage:
        "https://img.freepik.com/free-photo/tasty-beef-burger-ready-be-served_23-2148290587.jpg?w=1060&t=st=1695017405~exp=1695018005~hmac=7413418e9bf58927d19fc7c48b768373101d9572c69bff79857ed966a7a0f1ac",
      price: 15.49,
    },
    {
      id: 3,
      name: "Dummy Food 2",
      description: "This is dummy food description",
      backgroundImage:
        "https://img.freepik.com/free-photo/tasty-beef-burger-ready-be-served_23-2148290587.jpg?w=1060&t=st=1695017405~exp=1695018005~hmac=7413418e9bf58927d19fc7c48b768373101d9572c69bff79857ed966a7a0f1ac",
      price: 15.49,
    },
    {
      id: 4,
      name: "Dummy Food 2",
      description: "This is dummy food description",
      backgroundImage:
        "https://img.freepik.com/free-photo/tasty-beef-burger-ready-be-served_23-2148290587.jpg?w=1060&t=st=1695017405~exp=1695018005~hmac=7413418e9bf58927d19fc7c48b768373101d9572c69bff79857ed966a7a0f1ac",
      price: 15.49,
    },
    // ... Add more dummy products if necessary
  ];

  useEffect(() => {
    async function fetchData() {
      try {
        const restaurantResponse = await axios.get(
          `${BASE_URL}/api/restaurant/${restaurantId}/`
        );
        setRestaurant(restaurantResponse.data);

        const productsResponse = await axios.get(
          `${BASE_URL}/api/restaurant/${restaurantId}/products/`
        );
        setProducts(productsResponse.data);
      } catch (error) {
        console.error(
          `Error fetching details for restaurant ${restaurantId}:`,
          error
        );
        // Set dummy data on error
        setRestaurant(dummyRestaurant);
        setProducts(dummyProducts);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [restaurantId]);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="restaurant-detail">
      <div
        className="header"
        style={{ backgroundImage: `url(${restaurant.backgroundImage})` }}
      >
        <h1 className="rest-name">{restaurant.name}</h1>
      </div>
      <div>
        <h1 className="food"> Foods Available</h1>
      </div>
      <div className="menu-items">
        {products.map((item) => (
          <div key={item.id} className="menu-item">
            <div
              className="menu-item-image"
              style={{ backgroundImage: `url(${item.backgroundImage})` }}
            >
              <button className="add-button">Add</button>
            </div>
            <div className="menu-item-details">
              <h2>{item.name}</h2>
              <div className="description-price">
                <p>{item.description}</p>
                <p>${item.price.toFixed(2)}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RestaurantDetail;
