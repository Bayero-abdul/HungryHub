import React, { useState, useEffect } from "react";
import axios from "axios";
import "./accountPage.css";
import profilePicture from "../../assets/img_avatar.png";

const BASE_URL = "http://127.0.0.1:5000";

const AccountPage = () => {
  const [view, setView] = useState("account");
  const [editing, setEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fallback user and orders data
  const dummyUserInfo = {
    firstName: "Amsi",
    lastName: "Misi",
    email: "Amsi.misi@example.com",
    phone: "+251939038900",
    avatar: profilePicture,
  };

  const dummyOrders = [
    { id: 1, item: "Burger", price: 5.99 },
    { id: 2, item: "Pizza", price: 8.99 },
  ];

  const [userInfo, setUserInfo] = useState(dummyUserInfo); // Initialize with dummy data
  const [orders, setOrders] = useState(dummyOrders); // Initialize with dummy data

  useEffect(() => {
    async function fetchUserData() {
      try {
        const response = await axios.get(`${BASE_URL}/api/users/{userId}`);
        setUserInfo(response.data);
      } catch (err) {
        console.error("Failed to fetch user data.", err);
        setUserInfo(dummyUserInfo);
      } finally {
        setLoading(false);
      }
    }
    fetchUserData();
  }, []);

  useEffect(() => {
    if (view === "orders") {
      async function fetchUserOrders() {
        try {
          const response = await axios.get(
            `${BASE_URL}/api/users/{userId}/orders`
          );
          setOrders(response.data);
        } catch (err) {
          console.error("Failed to fetch orders.", err);
          setOrders(dummyOrders);
        }
      }
      fetchUserOrders();
    }
  }, [view]);

  const handleUpdate = async (updatedInfo) => {
    try {
      await axios.put(`${BASE_URL}/api/users/{userId}`, updatedInfo); // You need to pass the user ID here.
      setUserInfo(updatedInfo);
      setEditing(false);
    } catch (err) {
      setError("Failed to update user info.");
    }
  };

  const handleLogout = () => {
    // Handle logic to log out user, like clearing tokens.
    console.log("Logged out.");
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;
  return (
    <div className="accountPageContainer">
      <div className="sidebar">
        <div className="buttonWrapper" onClick={() => setView("account")}>
          <i className="fas fa-user"></i>
          Account
        </div>
        <div className="separator" />
        <div className="buttonWrapper" onClick={() => setView("orders")}>
          <i className="fas fa-basket-shopping"></i>
          Orders
        </div>
      </div>

      <div className="content">
        {view === "account" && (
          <div>
            {editing ? (
              <div className="editInfo">
                <p className="topText">Personal Information</p>
                <div className="imageAndButtons">
                  <img
                    src={userInfo.avatar}
                    alt="User profile"
                    className="editImage"
                  />
                  <div className="buttons">
                    <button className="btnSize">Change</button>
                    <button className="btnSize">Remove</button>
                  </div>
                  <button className="xBtn" onClick={() => setEditing(false)}>
                    Cancel
                  </button>
                </div>
                <div className="inputContainer">
                  <div className="inputGrid">
                    <div className="inputField">
                      <label>First Name:</label>
                      <input
                        className="inputSize"
                        defaultValue={userInfo.firstName}
                      />
                    </div>
                    <div className="inputField">
                      <label>Last Name:</label>
                      <input
                        className="inputSize"
                        defaultValue={userInfo.lastName}
                      />
                    </div>
                    <div className="inputField">
                      <label>Phone:</label>
                      <input
                        className="inputSize"
                        defaultValue={userInfo.phone}
                      />
                    </div>
                    <div className="inputField">
                      <label>Email:</label>
                      <input
                        className="inputSize"
                        defaultValue={userInfo.email}
                      />
                    </div>
                  </div>
                </div>
                <div className="bottomBtn">
                  <button
                    className="saveChange"
                    onClick={() => setEditing(false)}
                  >
                    Save Changes
                  </button>
                  <button className="logOut" onClick={() => {}}>
                    Log Out
                  </button>
                </div>
              </div>
            ) : (
              <div className="userInfo">
                <img src={userInfo.avatar} alt="User profile" />
                <button
                  onClick={() => setEditing(true)}
                  className="editAccountButton"
                >
                  Edit Account
                </button>
                <p>
                  <span>Name -</span> {userInfo.firstName} {userInfo.lastName}
                </p>
                <p>
                  <span>Email -</span> {userInfo.email}
                </p>
                <p>
                  <span>Phone -</span> {userInfo.phone}
                </p>
              </div>
            )}
          </div>
        )}

        {view === "orders" && <div>Your order list here...</div>}
      </div>
    </div>
  );
};

export default AccountPage;
