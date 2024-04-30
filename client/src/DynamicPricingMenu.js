import React, { useState, useEffect } from 'react';
import './DynamicPricingMenu.css';
import socketIOClient from 'socket.io-client';
import Item from './Item';


function DynamicPricingMenu() {
  const [showEnrolledProducts, setShowEnrolledProducts] = useState(false);
  const [pricingRecommendations, setPricingRecommendations] = useState([]);
  const [acceptedRecommendations, setAcceptedRecommendations] = useState([]);
  const [deniedRecommendations, setDeniedRecommendations] = useState([]);


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
    socket.on('hourly_suggestion_emitter', handleSocketEvent);

    return () => {
      socket.disconnect();
    };
  }, []);

  const handleAccept = (recommendation) => {
    fetch('http://localhost:5000/clear_recommendation', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ recommendation }),
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to clear recommendation');
      }
      // Update accepted recommendations in state
      setAcceptedRecommendations([...acceptedRecommendations, recommendation]);
      // Remove the accepted recommendation from pricingRecommendations
      setPricingRecommendations(prevState => {
        const newState = {...prevState};
        Object.keys(newState).forEach(category => {
          newState[category] = newState[category].filter(item => item !== recommendation);
        });
        return newState;
      });
    })
    .catch(error => {
      console.error('Error clearing recommendation:', error);
    });
  };

  const handleDeny = (recommendation) => {
    fetch('http://localhost:5000/clear_recommendation', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ recommendation }),
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to clear recommendation');
      }
      setAcceptedRecommendations([...acceptedRecommendations, recommendation]);
      setPricingRecommendations(prevState => {
        const newState = {...prevState};
        Object.keys(newState).forEach(category => {
          newState[category] = newState[category].filter(item => item !== recommendation);
        });
        return newState;
      });
    })
    .catch(error => {
      console.error('Error clearing recommendation:', error);
    });
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
      <p><strong>Name:</strong> <strong>{recommendation.name}</strong></p>
      <p>Category: {recommendation.category}</p>
      <p>Type: {recommendation.type.toUpperCase()}</p>
      <p>Action: {recommendation.action}</p>
      <p>Current Price: {(recommendation.current_price / 100).toFixed(2)}</p>
      <p className={recommendation.suggested_price > recommendation.current_price ? 'price-increase' : 'price-decrease'}>
        Suggested Price: {(recommendation.suggested_price / 100).toFixed(2)}
      </p>
      <button onClick={() => handleAccept(recommendation)} className="accept-button">Accept</button>
      <button onClick={() => handleDeny(recommendation)} className="deny-button">Deny</button>
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
