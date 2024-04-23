import React, { useState, useEffect } from 'react'; // Import useState hook from React library
import './DynamicPricingMenu.css'; // Import CSS file for styling
import socketIOClient from 'socket.io-client';

function DynamicPricingMenu() {
  // State to manage visibility of enrolled products popup
  const [showEnrolledProducts, setShowEnrolledProducts] = useState(false);
  const [pricingRecommendations, setPricingRecommendations] = useState([]);

  // Function to toggle visibility of enrolled products popup
  const toggleEnrolledProducts = () => {
    setShowEnrolledProducts(!showEnrolledProducts);
  };




  // Function to fetch recommendations from the server
  const fetchRecommendations = async () => {
    try {
      const response = await fetch('http://localhost:5000/get_recommendations');
      const data = await response.json();
      setPricingRecommendations(data);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
  };

  // Function to update recommendations when new data is emitted via Socket.IO
  const handleSocketEvent = (suggestions) => {
    setPricingRecommendations(suggestions);
  };

  useEffect(() => {
    // Fetch recommendations when the component mounts
    fetchRecommendations();

    // Set up Socket.IO connection
    const socket = socketIOClient('http://localhost:5000');

    // Listen for 'hourly_suggestions' event
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

      <div className="pricing-recommendations">
        {/* Placeholder for pricing recommendations */}
        <h3>High-Priority Price suggestions for unenrolled products</h3>
        {Object.keys(pricingRecommendations).map(category => (
        <div key={category}>
          <h4>{category}</h4>
          {pricingRecommendations[category].map((recommendation, index) => (
              <div key={index} className="recommendation">
              <p>Name: {recommendation.name} | Action: {recommendation.action} | Current Price: {(recommendation.current_price / 100).toFixed(2)} | Suggested Price: {(recommendation.suggested_price / 100).toFixed(2)} <button onClick={() => handleAccept(recommendation)}>Accept</button> <button onClick={() => handleDeny(recommendation)}>Deny</button> </p>
          </div>
          ))}
        </div>
      ))}
        </div>

    </div>
  );
}

export default DynamicPricingMenu;
