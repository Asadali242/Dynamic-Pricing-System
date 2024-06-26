import React, { useState, useEffect } from 'react';
import './DynamicPricingMenu.css';
import socketIOClient from 'socket.io-client';
import Item from './Item';


function DynamicPricingMenu() {
  const [showEnrolledProducts, setShowEnrolledProducts] = useState(false);
  const [enrolledProducts, setEnrolledProducts] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('hourly');
  const [pricingRecommendations, setPricingRecommendations] = useState([]);
  const [acceptedRecommendations, setAcceptedRecommendations] = useState([]);
  const [deniedRecommendations, setDeniedRecommendations] = useState([]);
  const [showPopup, setShowPopup] = useState(false);
  const [popupMessage, setPopupMessage] = useState('');
  const [totalUnitsSold, setTotalUnitsSold] = useState(null);
  const [totalSales, setTotaSales] = useState(null);

  

  useEffect(() => {
    // Fetch enrolled products when the component mounts
    fetchEnrolledProducts();
  }, []);

  const fetchEnrolledProducts = () => {
    fetch('http://localhost:5000/get_enrolled_products')
      .then(response => response.json())
      .then(data => {

        // Assuming the response is an object with 'seasonal' and 'hourly' keys
        const enrolledProductsData = data || {};
        console.log('Enrolled Products:', enrolledProductsData);
        setEnrolledProducts(enrolledProductsData);
      })
      .catch(error => {
        console.error('Error fetching enrolled products:', error);
      });
  };

  const openProductInfo = (id, pricingDetails) => {
    fetch('http://localhost:5000/price_change_history', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: id })  
    })
    .then(response => {
      if (!response.ok) {
          throw new Error('Failed to fetch price history');
      }
      return response.json();
    })
    .then(data => {
        if (data.success) {
          const priceHistory = data.price_history;
          const popupContent = priceHistory.map(entry => {
              const createdate = new Date(entry.createdate).toLocaleString();
              const priceUpdate = `priceBefore: ${entry.price_update.priceBefore}, priceAfter: ${entry.price_update.priceAfter}`;
              const rule = entry.rule ? `${JSON.stringify(entry.rule)}<br>` : 'N/A<br>'; 
              return `
                <tr>
                    <td><strong>createdate:</strong></td>
                    <td>${createdate}</td>
                </tr>
                <tr>
                    <td><strong>price_change:</strong></td>
                    <td>${priceUpdate}</td>
                </tr>
                <tr>
                    <td><strong>rule:</strong></td>
                    <td>${rule}</td>
                </tr>
            `;
          }).join('');  
          const popupWindow = window.open('', 'Popup_Window', 'width=800,height=400');
          popupWindow.document.write(`
          <style>
                    .popup-table {
                        border-collapse: collapse; 
                        width: 100%; 
                        padding: 10px;
                    }
                    .popup-table th, .popup-table td {
                        padding: 8px;
                        border: 1px solid #dddddd;
                        text-align: left;
                    }
                    .popup-table th {
                        background-color: #f2f2f2;
                        font-size: larger;
                    }
                    .pricing-rule-table {
                        margin-bottom: 20px; /* Add space below the pricing rule table */
                    }
                </style>
                <table class="popup-table pricing-rule-table">
                    <tr>
                        <th>Current Pricing Rule:</th>
                        <td>${pricingDetails ? JSON.stringify(pricingDetails) : 'N/A'}</td>
                    </tr>
                </table>
                <table class="popup-table">
                    <tr>
                        <th>Price Change History</th>
                    </tr>
                    ${popupContent}
                </table>
            `);
        } else {
            throw new Error(data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error.message);
        // Handle error as needed
    });
  };

  const renderHourlyProducts = () => {
    const hourlyProducts = enrolledProducts.hourly || [];
    return (
      <div>
        <h2>Hourly Products</h2>
        <table className="product-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Current Price</th>
              <th>Expires</th>
              <th>Timezone</th>
              <th>Price Max</th>
              <th>Price Min</th>
            </tr>
          </thead>
          <tbody>
            {hourlyProducts.map(([id, name, currentPrice, details], index) => {
              // End date based on create date and duration in days
              const expirationDate = new Date(details.expirationDate);
              return (
                <tr key={`hourly-${id}-${index}`}>
                  <td>
                    <a
                      href="#"
                      onClick={(e) => {
                        e.preventDefault(); // Prevent default anchor behavior
                        openProductInfo(id, details.hourlyPriceChanges); // Call function to open popup
                      }}
                    >
                      {name}
                    </a>
                  </td>
                  <td>{'$'+ currentPrice/100}</td>
                  <td>{expirationDate.toLocaleDateString()}</td>
                  <td>{details.timeZone}</td>
                  <td>{'$'+ Number(details.priceMax).toFixed(2)}</td>
                  <td>{'$'+ Number(details.priceMin).toFixed(2)}</td>
                  {/* additional columns for other details */}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    );
  };
  
  const renderSeasonalProducts = () => {
    const seasonalProducts = enrolledProducts.seasonal || [];
    return (
      <div>
        <h2>Seasonal Products</h2>
        <table className="product-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Current Price</th>
              <th>Expires</th>
              <th>Price Max</th>
              <th>Price Min</th>
              {/* Add additional column headers as needed */}
            </tr>
          </thead>
          <tbody>
            {seasonalProducts.map(([id, name, currentPrice, details], index) => {
              // Calculate end date based on create date and duration in years
              const expirationDate = new Date(details.expirationDate);
              return (
                <tr key={`seasonal-${id}-${index}`}>
                  <td>
                    <a
                      href="#"
                      onClick={(e) => {
                        e.preventDefault(); // Prevent default anchor behavior
                        openProductInfo(id, details.seasonalPriceChanges); // Call function to open popup
                      }}
                    >
                      {name}
                    </a>
                  </td>
                  <td>{'$'+ currentPrice/100}</td>
                  <td>{expirationDate.toLocaleDateString()}</td>
                  <td>{'$'+ Number(details.priceMax).toFixed(2)}</td>
                  <td>{'$'+ Number(details.priceMin).toFixed(2)}</td>
                  {/* Add additional columns for other details */}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    );
  };

  const handleCategoryClick = (category) => {
    setSelectedCategory(category);
  };

  const renderCategoryHeaders = () => {
    return (
      <div className="category-headers">
        <button className={selectedCategory === 'hourly' ? 'selected' : ''} onClick={() => handleCategoryClick('hourly')}>Hourly</button>
        <button className={selectedCategory === 'seasonal' ? 'selected' : ''} onClick={() => handleCategoryClick('seasonal')}>Seasonal</button>
        {/* Add more category buttons as needed */}
      </div>
    );
  };
  

  const fetchTotalUnitsSold = async () => {
    try {
      const response = await fetch('http://localhost:5000/get_total_units_sold');
      const data = await response.json();
      setTotalUnitsSold(data);
    } catch (error) {
      setTotalUnitsSold('Error fetching data');
    }
  };

  useEffect(() => {
    fetchTotalUnitsSold(); 
  }, []);

  const fetchTotalSales = async () => {
    try {
      const response = await fetch('http://localhost:5000/get_total_sales');
      const data = await response.json();
      setTotaSales(data);
    } catch (error) {
      setTotaSales('Error fetching data');
    }
  };

  useEffect(() => {
    fetchTotalSales(); 
  }, []);

  const fetchRecommendations = async () => {
    try {
      const response = await fetch('http://localhost:5000/get_recommendations');
      const data = await response.json();
      setPricingRecommendations(data);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
  };

  const PopupMessage = () => {
    if (!showPopup) return null;

    return (
      <div className="popup-container">
        <div className="popup-message">
          {popupMessage}
          <button className="exit-button" onClick={() => setShowPopup(false)}>Exit</button>
        </div>
      </div>
    );
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
      setPopupMessage('The suggestion has been accepted.');
      setShowPopup(true);
    })
    .catch(error => {
      console.error('Error clearing recommendation:', error);
    });

    fetch('http://localhost:5000/suggestion_price_update', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ recommendation }), 
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to update price based on recommendation');
      }
    })
    .catch(error => {
      console.error('Error updating price based on recommendation:', error);
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
      setPopupMessage('The suggestion has been denied.');
      setShowPopup(true);
    })
    .catch(error => {
      console.error('Error clearing recommendation:', error);
    });
  };

  // Function to sort the recommendations based on the absolute difference between current price and suggested price
  const sortRecommendations = (recommendations) => {
    return recommendations.sort((a, b) => Math.abs(parseFloat(b.Percentage)) - Math.abs(parseFloat(a.Percentage)));
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
      <p className={recommendation.Percentage.startsWith('-') ? 'price-decrease' : 'price-increase'}>
        Percentage Change: {recommendation.Percentage}
      </p>
      <p>Current Price: ${(recommendation.current_price / 100).toFixed(2)}</p>
      <p className={recommendation.suggested_price > recommendation.current_price ? 'price-increase' : 'price-decrease'}>
        Suggested Price: ${(recommendation.suggested_price / 100).toFixed(2)}
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
            <p className="value-text">{totalUnitsSold ? totalUnitsSold : 'Loading...'}</p>
          </div>
          <div className="dashboard-section">
            <h3>Total Sales</h3>
            <p className="value-text">{totalSales ? `$${totalSales.toLocaleString()}` : 'Loading...'}</p>
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
          <div className="popup-content" style={{ maxHeight: '85vh', overflowY: 'auto' }}>
            <button className="exit-button" onClick={() => setShowEnrolledProducts(false)}>Exit</button>
            {renderCategoryHeaders()}
            {selectedCategory === 'hourly' && renderHourlyProducts()}
            {selectedCategory === 'seasonal' && renderSeasonalProducts()}
          </div>
        </div>
      )}

      <div className="pricing-recommendations">
        <h3>Top 10 Price Suggestions for Products Not Enrolled in Manual Rules</h3>
          {/* Render top recommendations */}
          {renderTopRecommendations()}
          <PopupMessage />
        </div>
      </div>
  );
}

export default DynamicPricingMenu;
