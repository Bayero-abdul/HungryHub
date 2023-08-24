import React from 'react';

import Header from './Header';
import Footer from './Footer';
import Routes from "../routes/Routers";
// import { BrowseRouter, Routes, Route } from 'react-router-dom'
import { AuthProvider } from '../context/AuthProvider';

function Layout() {
  return (
    <div className="App">
        <AuthProvider>
            <Header />
            <div style={{padding: "2rem", display: "flex", justifyContent:"center", alignItems:'center'}}>
                <Routes />
            </div>
            <Footer /> 
        </AuthProvider>
    </div>
  );
}

export default Layout;
