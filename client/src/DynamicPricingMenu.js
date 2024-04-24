import React, { useState, useEffect } from 'react';
import './DynamicPricingMenu.css';
import socketIOClient from 'socket.io-client';

function DynamicPricingMenu() {
  const [showEnrolledProducts, setShowEnrolledProducts] = useState(false);
  const [pricingRecommendations, setPricingRecommendations] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [showPopup, setShowPopup] = useState(false);

  const categories = ['Snacks', 'Ice Cream', 'Chicken', 'Candy', 'Beverages'];

  const fetchRecommendations = async () => {
    try {
      const response = await fetch('http://localhost:5000/get_recommendations');
      const data = await response.json();
      setPricingRecommendations(data);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
  };

  const handleSocketEvent = (suggestions) => {
    setPricingRecommendations(suggestions);
  };

  useEffect(() => {
    fetchRecommendations();

    const socket = socketIOClient('http://localhost:5000');
    socket.on('hourly_suggestion_updater', handleSocketEvent);

    return () => {
      socket.disconnect();
    };
  }, []);

  const handleAccept = (recommendation) => {
    // Logic to handle accepting recommendation
  };

  const handleDeny = (recommendation) => {
    // Logic to handle denying recommendation
  };

  const handleCategoryChange = (category) => {
    setSelectedCategory(category);
    setShowPopup(false);
  };

  const renderCategoryButtons = () => {
    return categories.map(category => (
      <button key={category} onClick={() => handleCategoryChange(category)}>
        {category}
      </button>
    ));
  };

  const clearCategory = () => {
    setSelectedCategory(null);
  };

  return (
    <div>
      {/* Dashboard */}
      <div className="dashboard">
        <h2>Dashboard</h2>
        <div className="dashboard-sections">
          <div className="dashboard-section">
            <h3>Products Sold</h3>
          </div>
          <div className="dashboard-section">
            <h3>Missed Sales</h3>
          </div>
          <div className="dashboard-section">
            <h3>Profit</h3>
          </div>
          <div className="dashboard-section">
            <h3>Total Sales</h3>
          </div>
          <div className="dashboard-section">
            <h3>Margin</h3>
          </div>
        </div>
      </div>

      {/* View Enrolled Products button */}
      <div className="view-enrolled-products-button-container">
        <button className="view-enrolled-products-button" onClick={() => setShowEnrolledProducts(!showEnrolledProducts)}>
          View Enrolled Products
        </button>
      </div>

      {/* Enrolled Products popup */}
      {showEnrolledProducts && (
        <div className="popup">
          <div className="popup-content">
            <button className="exit-button" onClick={() => setShowEnrolledProducts(false)}>Exit</button>
          </div>
        </div>
      )}

      <div className="pricing-recommendations">
        <div className="filter-container">
          <button className="filter-button" onClick={() => setShowPopup(true)}>Filter</button>
          {showPopup && (
            <div className="popup-background">
              <div className="category-popup">
                <h3>Select Category</h3>
                <div className="category-buttons">
                  {renderCategoryButtons()}
                </div>
                <button onClick={() => setShowPopup(false)}>Close</button>
              </div>
            </div>
          )}
          {selectedCategory && <button className="clear-button" onClick={clearCategory}>Clear</button>}
        </div>
        <h3>High-Priority Price Suggestions for Unenrolled Products</h3>
        {Object.keys(pricingRecommendations).map(category => (
          <div key={category} className="category-box">
            <h4>{category}</h4>
            {pricingRecommendations[category].map((recommendation, index) => (
              <div key={index} className="recommendation">
                <p>Name: {recommendation.name} | Type: {recommendation.type} | Action: {recommendation.action} | Current Price: {(recommendation.current_price / 100).toFixed(2)} | Suggested Price: {(recommendation.suggested_price / 100).toFixed(2)} <button onClick={() => handleAccept(recommendation)}>Accept</button> <button onClick={() => handleDeny(recommendation)}>Deny</button> </p>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

export default DynamicPricingMenu;
