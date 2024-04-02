import React, { useState } from 'react'; // Import useState hook from React library
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
        {/* Container for dashboard sections */}
        <div className="dashboard-sections">
          {/* Individual dashboard sections */}
          <div className="dashboard-section">
            <h3>Products Sold</h3>
            {/* Content for Products Sold section */}
          </div>
          <div className="dashboard-section">
            <h3>Missed Sales</h3>
            {/* Content for Missed Sales section */}
          </div>
          <div className="dashboard-section">
            <h3>Profit</h3>
            {/* Content for Profit section */}
          </div>
          <div className="dashboard-section">
            <h3>Total Sales</h3>
            {/* Content for Total Sales section */}
          </div>
          <div className="dashboard-section">
            <h3>Margin</h3>
            {/* Content for Margin section */}
          </div>
        </div>
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
