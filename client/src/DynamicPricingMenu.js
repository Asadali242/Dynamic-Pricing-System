import React, { useState } from 'react';
import './DynamicPricingMenu.css'; // Import CSS file for styling

function DynamicPricingMenu() {
  // State to manage visibility of enrolled products popup
  const [showEnrolledProducts, setShowEnrolledProducts] = useState(false);

  // Function to toggle visibility of enrolled products popup
  const toggleEnrolledProducts = () => {
    setShowEnrolledProducts(!showEnrolledProducts);
  };

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
          </div>
        </div>
      )}
    </div>
  );
}

export default DynamicPricingMenu;
