import React from 'react';
import './RestaurantDetail.css';

function RestaurantDetail({ restaurant }) {
    return (
        <div className="restaurant-detail">
           
            <div className="header" style={{ backgroundImage: `url(${restaurant.backgroundImage})` }}>
                <h1 className='rest-name'>{restaurant.name}</h1>
            </div>
            <div >
                <h1 className='food'> Foods Available</h1>
            </div>
            <div className="menu-items">
                {restaurant.menu.map(item => (
                    <div key={item.id} className="menu-item">
                        <div className="menu-item-image" style={{ backgroundImage: `url(${item.backgroundImage})` }}>
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
