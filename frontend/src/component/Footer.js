import React from 'react';

const Footer = () => {
  return (
    <footer style={{ backgroundColor: '#133b38', color: 'white', padding: '1rem', textAlign: 'center' }}>
      © {new Date().getFullYear()} Your Company. All Rights Reserved.
    </footer>
  );
};

export default Footer;
