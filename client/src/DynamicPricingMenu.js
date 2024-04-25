import React, { useState, useEffect } from 'react';
import './DynamicPricingMenu.css';
import socketIOClient from 'socket.io-client';

function DynamicPricingMenu() {
  const [showEnrolledProducts, setShowEnrolledProducts] = useState(false);
  const [pricingRecommendations, setPricingRecommendations] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [showPopup, setShowPopup] = useState(false);
  const [acceptedRecommendations, setAcceptedRecommendations] = useState([]);
  const [deniedRecommendations, setDeniedRecommendations] = useState([]);

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
    setAcceptedRecommendations([...acceptedRecommendations, recommendation]);
    // Remove the recommendation from denied list if it exists
    setDeniedRecommendations(deniedRecommendations.filter(item => item !== recommendation));
  };

  const handleDeny = (recommendation) => {
    // Logic to handle denying recommendation
    setDeniedRecommendations([...deniedRecommendations, recommendation]);
    // Remove the recommendation from accepted list if it exists
    setAcceptedRecommendations(acceptedRecommendations.filter(item => item !== recommendation));
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

  // Function to sort the recommendations based on the absolute difference between current price and suggested price
  const sortRecommendations = (recommendations) => {
    return recommendations.sort((a, b) => Math.abs(a.current_price - a.suggested_price) - Math.abs(b.current_price - b.suggested_price));
  };

  // Function to render the top 10 recommendations for the selected category
  const renderTopRecommendations = () => {
    const allRecommendations = Object.values(pricingRecommendations).flat();
    const sortedRecommendations = sortRecommendations(allRecommendations);
    const filteredRecommendations = sortedRecommendations.filter(recommendation =>
      !acceptedRecommendations.includes(recommendation) && !deniedRecommendations.includes(recommendation)
    );
    const topRecommendations = filteredRecommendations.slice(0, 10);

    return (
      <div className="category-box">
        {topRecommendations.map((recommendation, index) => (
          <div key={index} className="recommendation">
            <p>
              Name: {recommendation.name} | Category: {recommendation.category} | Type: {recommendation.type.toUpperCase()} |
              Action: {recommendation.action} | Current Price: {(recommendation.current_price / 100).toFixed(2)} |
              Suggested Price: {(recommendation.suggested_price / 100).toFixed(2)}
              <button onClick={() => handleAccept(recommendation)}>Accept</button>
              <button onClick={() => handleDeny(recommendation)}>Deny</button>
            </p>
          </div>
        ))}
      </div>
    );
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
        <h3>Top 10 Price Suggestions for Unenrolled Products</h3>
          {/* Render top recommendations */}
          {renderTopRecommendations()}
        </div>
      </div>
  );
}

export default DynamicPricingMenu;
