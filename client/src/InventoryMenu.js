import React, { useState } from 'react';
import './DynamicPricingMenu.css'; // Import CSS file for styling

function DynamicPricingMenu() {
  // State to manage visibility of enrolled products popup
  const [showEnrolledProducts, setShowEnrolledProducts] = useState(false);
  // State to hold categories
  const [categories, setCategories] = useState([]);

  // Function to toggle visibility of enrolled products popup
  const toggleEnrolledProducts = () => {
    setShowEnrolledProducts(!showEnrolledProducts);
  };

  // Function to handle category filter
  const handleCategoryFilter = () => {
    setCategories([
      'Grocery',
      'Hot Foods',
      'Ice Cream',
      'Medicine',
      'Sandwiches',
      'Soda',
      'Water',
      'Snacks',
      'Health',
      'Household'
    ]);
  };

  // Dummy data for enrolled products
  const enrolledProducts = [
    { id: 1, name: 'Product A', category: 'Grocery' },
    { id: 2, name: 'Product B', category: 'Hot Foods' },
    { id: 3, name: 'Product C', category: 'Ice Cream' },
    { id: 4, name: 'Product D', category: 'Medicine' },
    { id: 5, name: 'Product E', category: 'Sandwiches' },
    { id: 6, name: 'Product F', category: 'Soda' },
    { id: 7, name: 'Product G', category: 'Water' },
    { id: 8, name: 'Product H', category: 'Snacks' },
    { id: 9, name: 'Product I', category: 'Health' },
    { id: 10, name: 'Product J', category: 'Household' },
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

            {/* Category filter button */}
            <button className="category-button" onClick={handleCategoryFilter}>Category</button>

            {/* Calendar filter */}
            <input type="date" className="calendar-filter" placeholder="Select date" />

            {/* Search bar */}
            <input type="text" className="search-bar" placeholder="Search" />

            {/* Categories list */}
            <div className="categories-list">
              <h3>Categories</h3>
              <ul>
                {categories.map(category => (
                  <li key={category}>{category}</li>
                ))}
              </ul>
            </div>

            {/* Enrolled products list */}
            <div className="enrolled-products-list">
              <h3>Enrolled Products</h3>
              <ul>
                {enrolledProducts.map(product => (
                  <li key={product.id}>{product.name} - {product.category}</li>
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
