import React, { useState } from 'react';
import './DynamicPricingMenu.css'; // Import CSS file for styling

function DynamicPricingMenu() {
  // State to manage visibility of enrolled products popup
  const [showEnrolledProducts, setShowEnrolledProducts] = useState(false);

  // Function to toggle visibility of enrolled products popup
  const toggleEnrolledProducts = () => {
    setShowEnrolledProducts(!showEnrolledProducts);
  };

  // Dummy data for enrolled products
  const enrolledProducts = [
    { id: 1, name: 'Product A', price: 10 },
    { id: 2, name: 'Product B', price: 15 },
    { id: 3, name: 'Product C', price: 5 },
    { id: 4, name: 'Product D', price: 20 },
    { id: 5, name: 'Product E', price: 8 },
    { id: 6, name: 'Product F', price: 2 },
    { id: 7, name: 'Product G', price: 1 },
    { id: 8, name: 'Product H', price: 7 },
    { id: 9, name: 'Product I', price: 12 },
    { id: 10, name: 'Product J', price: 18 },
  ];

  return (
    <div>
      {/* Dashboard */}
      <div className="dashboard">
        <h2>Dashboard</h2>
        <p>Metrics coming soon</p>
      </div>

      {/* View Enrolled Products button */}
      <div className="view-enrolled-products-button-container">
        <button className="view-enrolled-products-button" onClick={toggleEnrolledProducts}>
          View Enrolled Products
        </button>
      </div>

      {/* Enrolled Products popup */}
      {showEnrolledProducts && (
        <div className="popup">
          <div className="popup-content">
            {/* Exit button */}
            <button className="exit-button" onClick={toggleEnrolledProducts}>Exit</button>

            {/* Filter buttons */}
            <div className="filter-buttons">
              <button className="calendar-button">Calendar</button>
              <input type="text" placeholder="Search..." className="search-bar" />
              <button className="filter-button">Filter by Category</button>
            </div>

            {/* Enrolled products list */}
            <div className="enrolled-products-list">
              <h3>Products</h3>
              <ul>
                {enrolledProducts.map(product => (
                  <li key={product.id}>
                    {product.name} - ${product.price}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default DynamicPricingMenu;
