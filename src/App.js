import React from "react";
import { BrowserRouter as Router, Route, Link, Routes } from "react-router-dom";
import "./App.css";
import RestaurantDetail from "./pages/RestaurantDetail/RestaurantDetail";
import AccountPage from "./pages/accountPage/accountPage";

function App() {
  // Hardcoded restaurant ID for demonstration.
  // In a real-world scenario, you might get this from user input or another source.
  const restaurantId = 1;

  return (
    <Router>
      <div className="App">
        <div className="navbar">
          <Link className="nav-link" to="/">
            Home
          </Link>
          <Link className="nav-link" to="/restaurant">
            Restaurant
          </Link>
          <Link className="nav-link" to="/account">
            Account
          </Link>
        </div>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route
            path="/restaurant"
            element={<RestaurantDetail restaurantId={restaurantId} />}
          />
          <Route path="/account" element={<AccountPage />} />
        </Routes>
      </div>
    </Router>
  );
}

// Simple homepage component
function Home() {
  return (
    <div>
      <h1>Welcome to the Homepage</h1>
      <p>Click on the links above to navigate.</p>
    </div>
  );
}

export default App;
