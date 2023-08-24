import React from 'react';
import Container from '@mui/material/Container';
import Footer from '../component/Footer';
import Header from '../component/Header';
import useRefreshToken from '../hooks/useRefresh';

const Home = () => {
  const resfresh = useRefreshToken();

  return (
    <div style={{ backgroundColor: '#2C5F5B', minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Container style={{ flex: '1', backgroundColor: '#EAEAEA', paddingTop: '2rem' }}>
        <button onClick={() => resfresh()}>refresh</button>
      </Container>
    </div>
  );
};

export default Home;
