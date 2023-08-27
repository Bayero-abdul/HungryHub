import logo from './logo.svg';
import './App.css';
import RestaurantDetail from './pages/RestaurantDetail/RestaurantDetail';

function App() {
  const restaurant = {
    name: "Happy burger",
    backgroundImage: "https://img.freepik.com/free-photo/exploding-burger-with-vegetables-melted-cheese-black-background-generative-ai_157027-1734.jpg?w=2000&t=st=1693155989~exp=1693156589~hmac=49eed7c9590522e4cee4e667f7871b964a88dcbd355dff42f131cdae24bb2e84",
    menu: [
      {id: 1, name: "burger", description: "cheese", price: 10.50, backgroundImage:"https://img.freepik.com/free-photo/big-sandwich-hamburger-with-juicy-beef-burger-cheese-tomato-red-onion-wooden-table_2829-19631.jpg?w=2000&t=st=1693151783~exp=1693152383~hmac=5392722df03d607c86ebc98dd07aa7e3e5c43fefe11ad7cae9d67f4997fed506"},
      {id: 2, name: "burger", description: "cheese", price: 10.50,backgroundImage:"https://img.freepik.com/free-photo/big-sandwich-hamburger-with-juicy-beef-burger-cheese-tomato-red-onion-wooden-table_2829-19631.jpg?w=2000&t=st=1693151783~exp=1693152383~hmac=5392722df03d607c86ebc98dd07aa7e3e5c43fefe11ad7cae9d67f4997fed506"},
    
      {id: 3, name: "burger", description: "cheese", price: 10.50, backgroundImage:"https://img.freepik.com/free-photo/big-sandwich-hamburger-with-juicy-beef-burger-cheese-tomato-red-onion-wooden-table_2829-19631.jpg?w=2000&t=st=1693151783~exp=1693152383~hmac=5392722df03d607c86ebc98dd07aa7e3e5c43fefe11ad7cae9d67f4997fed506"},
      {id: 4, name: "burger", description: "cheese", price: 10.50,backgroundImage:"https://img.freepik.com/free-photo/big-sandwich-hamburger-with-juicy-beef-burger-cheese-tomato-red-onion-wooden-table_2829-19631.jpg?w=2000&t=st=1693151783~exp=1693152383~hmac=5392722df03d607c86ebc98dd07aa7e3e5c43fefe11ad7cae9d67f4997fed506"},
    ] 

  }
  return (
    <div className="App">
      <RestaurantDetail restaurant = {restaurant} />
      
    </div>
  );
}

export default App;
