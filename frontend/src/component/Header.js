import React, { useContext } from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import { Button } from "@mui/material";
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import Typography from '@mui/material/Typography';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthProvider';

const Header = () => {
  const { auth, setAuth } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    setAuth({}); // Clear the authentication state
    sessionStorage.removeItem("Tokens"); // Remove tokens from local storage
    navigate("/login");
  };

  return (
    <AppBar position="static" style={{ backgroundColor: '#133b38' }}>
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          <Link to="/home" style={{ textDecoration: 'none', color: 'inherit' }}>
            HungryHub
          </Link>
        </Typography>

        {/* Basket Icon */}
        <IconButton color="inherit" style={{ marginRight: '16px' }}>
          <ShoppingCartIcon />
        </IconButton>

        {auth.user ? (
          <Button onClick={handleLogout} style={{ color: 'white', marginRight: '16px' }}>
            Logout
          </Button>
        ) : (
          <>
            <Link to="/login" style={{ color: 'white', textDecoration: 'none', marginRight: '16px' }}>
              <Button>
                Login
              </Button>
            </Link>
            <Link to="/register" style={{ color: 'white', textDecoration: 'none', marginRight: '16px' }}>
              <Button>
                Register
              </Button>
            </Link>
          </>
        )}
        <Link to="/payment" style={{ color: 'white', textDecoration: 'none' }}>
          <Button>
            Payment
          </Button>
        </Link>
      </Toolbar>
    </AppBar>
  );
};

export default Header;