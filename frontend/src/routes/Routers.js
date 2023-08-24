import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";

import Register from '../pages/Register';
import Login from '../pages/Login';
import Home from "../pages/Home"; 
import Payment from "../pages/Payment";

import RequireAuth from "../component/RequireAuth";

const Routers = () => {
    return (
      <Routes>
        <Route path="/" element={<Navigate to="/home" />} />
        <Route path="/home" element={<Home />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route element={<RequireAuth />}>
          <Route path="/payment" element={<Payment />} />
        </Route>
      </Routes>
    )
}

export default Routers;