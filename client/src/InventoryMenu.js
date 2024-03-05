import React, { useState } from 'react';

function InventoryMenu() {
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [showPopup, setShowPopup] = useState(false);
  const [showCreateRuleModal, setShowCreateRuleModal] = useState(false);
  const [ruleType, setRuleType] = useState(null);
  const [priceMaximum, setPriceMaximum] = useState('');
  const [priceMinimum, setPriceMinimum] = useState('');
  const [duration, setDuration] = useState('');

  

  const categories = [
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
  ];

  const handleCategoryChange = (category) => {
    setSelectedCategory(category);
    setShowPopup(false);
  };

  const clearCategory = () => {
    setSelectedCategory(null);
  };

  const renderCategoryButtons = () => {
    return categories.map(category => (
      <button key={category} onClick={() => handleCategoryChange(category)}>
        {category}
      </button>
    ));
  };

  const handleCreateRuleClick = () => {
    setShowCreateRuleModal(true);
  };

  const handleCloseModal = () => {
    setShowCreateRuleModal(false);
    setRuleType(null); 
    setPriceMaximum('');
    setPriceMinimum('');
    setDuration('');
  };

  const handleRuleTypeChange = (event) => {
    setRuleType(event.target.value);
  };

  const handleSaveEdit = () => {
    // Logic for saving edits
    handleCloseModal(); // Close modal after saving
  };


  return (
    <div className="inventory-menu">
      <h2>Inventory</h2>
      {selectedCategory && <p>Filtering by: {selectedCategory}</p>}
      <div className="item-list">
        <ul>
          <li>{selectedCategory ? `Item info from '${selectedCategory}'` : 'Item 1'}</li>
          <li>{selectedCategory ? `Item info from '${selectedCategory}'` : 'Item 2'}</li>
          <li>{selectedCategory ? `Item info from '${selectedCategory}'` : 'Item 3'}</li>
          <li>{selectedCategory ? `Item info from '${selectedCategory}'` : 'Item 4'}</li>
          <li>{selectedCategory ? `Item info from '${selectedCategory}'` : 'Item 5'}</li>
          <li>{selectedCategory ? `Item info from '${selectedCategory}'` : 'Item 6'}</li>
          <li>{selectedCategory ? `Item info from '${selectedCategory}'` : 'Item 7'}</li>
          <li>{selectedCategory ? `Item info from '${selectedCategory}'` : 'Item 8'}</li>
          <li>{selectedCategory ? `Item info from '${selectedCategory}'` : 'Item 9'}</li>
          <li>{selectedCategory ? `Item info from '${selectedCategory}'` : 'Item 10'}</li>
        </ul>
      </div>
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
        {selectedCategory && (
          <button className="create-dynamic-pricing-rule-button" onClick={handleCreateRuleClick}>
            Create Dynamic Pricing Rule
          </button>
        )}
      </div>
      {showCreateRuleModal && (
        <div className="modal">
          <div className="modal-content">
            <h3>Create a rule for {selectedCategory}</h3>
            <label htmlFor="ruleType">Rule Type:</label>
            <select id="ruleType" value={ruleType} onChange={handleRuleTypeChange}>
              <option value="">Select Rule Type</option>
              <option value="TimeOfDay">Time of Day Rule</option>
              <option value="Seasonality">Seasonality Rule</option>
            </select>
            {ruleType === 'TimeOfDay' && (
              <div>
                <div>
                  <label htmlFor="priceMaximum">Price Maximum ($):</label>
                  <input
                    type="text"
                    id="priceMaximum"
                    value={priceMaximum}
                    onChange={(e) => setPriceMaximum(e.target.value)}
                  />
                </div>
                <div>
                  <label htmlFor="priceMinimum">Price Minimum ($):</label>
                  <input
                    type="text"
                    id="priceMinimum"
                    value={priceMinimum}
                    onChange={(e) => setPriceMinimum(e.target.value)}
                  />
                </div>
                <div>
                  <label htmlFor="duration">Duration (weeks):</label>
                  <input
                    type="text"
                    id="duration"
                    value={duration}
                    onChange={(e) => setDuration(e.target.value)}
                  />
                </div>
              </div>
            )}
            {ruleType === 'Seasonality' && (
              <div>
                {/* Content for Seasonality rule */}
                <p>Select season...</p>
              </div>
            )}
            {ruleType && (
              <div>
                <button onClick={handleSaveEdit}>Save Edit</button>
                <button onClick={handleCloseModal}>Cancel</button>
              </div>
            )}
          </div>
        </div>
      )}
      <div className="pricing-recommendations">
        {/* Placeholder for pricing recommendations */}
        <h3>Pricing Recommendations</h3>
        <p>Algo generated reccomendations go here</p>
      </div>
    </div>
  );
}

export default InventoryMenu;