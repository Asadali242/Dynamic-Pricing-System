import React, { useState } from 'react';

function InventoryMenu() {
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [showPopup, setShowPopup] = useState(false);

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
        {selectedCategory && <button className="create-dynamic-pricing-rule-button">Create Dynamic Pricing Rule</button>}
      </div>
      <div className="pricing-recommendations">
        {/* Placeholder for pricing recommendations */}
        <h3>Pricing Recommendations</h3>
        <p>Algo generated reccomendations go here</p>
      </div>
    </div>
  );
}

export default InventoryMenu;
