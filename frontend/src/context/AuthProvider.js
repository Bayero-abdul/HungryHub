import React from 'react';
import {createContext, useState} from "react";

export const AuthContext = createContext({});

export const AuthProvider = ({ children }) => {
    const [auth, setAuth] = useState({});

    // let logoutUser = () => {
    //     const response = api.post("/auth/logout", {
    //       Authorization:
    //         "Bearer " +
    //         JSON.parse(localStorage.getItem("authTokens")).accessToken.trim(),
    //     });
    //     setAuthTokens("xxx");
    //     setUser("xxx");
    //     localStorage.removeItem("authTokens");
    //     api.defaults.headers["Authorization"] = null;
    //     navigate("/login");
    // };

    return (
        <AuthContext.Provider value={{ auth, setAuth }}>
            {children}
        </AuthContext.Provider>
    )   
}