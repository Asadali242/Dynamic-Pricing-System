import React, { useState, useEffect } from 'react';

function InventoryMenu() {
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [showPopup, setShowPopup] = useState(false);
  const [showCreateRuleModal, setShowCreateRuleModal] = useState(false);
  const [ruleType, setRuleType] = useState(null);
  const [priceMaximum, setPriceMaximum] = useState('');
  const [priceMinimum, setPriceMinimum] = useState('');
  const [duration, setDuration] = useState('');
  const [hourRules, setHourRules] = useState([]);
  const [isValidTimeFormat, setIsValidTimeFormat] = useState(true);
  const [seasonRules, setSeasonRules] = useState([]);
  const [validPriceMaximum, setValidPriceMaximum] = useState(false);
  const [validPriceMinimum, setValidPriceMinimum] = useState(false);
  const [validDuration, setValidDuration] = useState(false);
  const [validHourRules, setValidHourRules] = useState(false);
  const [validSeasonRules, setValidSeasonRules] = useState(false);
  const [timezone, setTimezone] = useState('EST');
  
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

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (showCreateRuleModal && !event.target.closest('.inventory-menu')) {
        handleCloseModal();
      }
    };

    document.body.addEventListener('click', handleClickOutside);

    return () => {
      document.body.removeEventListener('click', handleClickOutside);
    };
  }, [showCreateRuleModal]);
  
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
    setTimezone('EST');
    setHourRules([]);
    setIsValidTimeFormat(true);
    setSeasonRules([]);
  };

  
  const handleRuleTypeChange = (event) => {
    setRuleType(event.target.value);

    if (event.target.value === 'Seasonality') {
      setSeasonRules([
        { season: 'Summer', type: '+', percent: '' },
        { season: 'Fall', type: '+', percent: '' },
        { season: 'Winter', type: '+', percent: '' },
        { season: 'Spring', type: '+', percent: '' }
      ]);
    }
  };

  

  const handleSaveEdit = () => {
    let isValid = true;

    const hasPlaceholderHour = hourRules.some(rule => rule.timestamp === "" /*|| ":00"*/);
    if (hasPlaceholderHour) {
      isValid = false;
    }
    // Check if price maximum is a valid positive number
    if (isNaN(parseFloat(priceMaximum)) || parseFloat(priceMaximum) < 0) {
        setValidPriceMaximum(false);
        isValid = false;
    } else {
        setValidPriceMaximum(true);
    }

    // Check if price minimum is a valid positive number
    if (isNaN(parseFloat(priceMinimum)) || parseFloat(priceMinimum) < 0) {
        setValidPriceMinimum(false);
        isValid = false;
    } else {
        setValidPriceMinimum(true);
    }

    // Check if duration is a valid positive number
    if (isNaN(parseFloat(duration)) || parseFloat(duration) < 0) {
        setValidDuration(false);
        isValid = false;
    } else {
        setValidDuration(true);
    }

    // Check if all hour rules have valid percentages
    const validHourRules = hourRules.every(rule => !isNaN(parseFloat(rule.percent)) && parseFloat(rule.percent) >= 0);
    if (!validHourRules) {
        setValidHourRules(false);
        isValid = false;
    } else {
        setValidHourRules(true);
    }

    // Check if all season rules have valid percentages
    const validSeasonRules = seasonRules.every(rule => !isNaN(parseFloat(rule.percent)) && parseFloat(rule.percent) >= 0);
    if (!validSeasonRules) {
        setValidSeasonRules(false);
        isValid = false;
    } else {
        setValidSeasonRules(true);
    }

    // Check if there are no repeated hours of the day
    const selectedHours = hourRules.map(rule => rule.timestamp.split(':')[0]);
    const hasRepeatedHours = selectedHours.some((hour, index) => selectedHours.indexOf(hour) !== index);
    if (hasRepeatedHours) {
        setValidHourRules(false);
        isValid = false;
    }
    if (isValid) {
      console.log(JSON.stringify({
        ruleType,
        category: selectedCategory,
        duration,
        priceMinimum,
        priceMaximum,
        timezone,
        hourlyPriceChanges: hourRules,
        seasonalPriceChanges: seasonRules
    }),)
      fetch('http://localhost:5000/save_rule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            ruleType,
            category: selectedCategory,
            duration,
            priceMinimum,
            priceMaximum,
            timezone,
            hourlyPriceChanges: hourRules,
            seasonalPriceChanges: seasonRules
        }),
      })
      .then(response => response.json())
      .then(data => {
          console.log('Success:', data);
          handleCloseModal(); // Close modal after saving
      })
      .catch((error) => {
          console.error('Error:', error);
      });
      handleCloseModal(); 
    }
};



  const handleAddHourRule = () => {
    if (hourRules.length < 24) {
      setHourRules([...hourRules, { timestamp: '', type: '+', percent: '' }]);
    }
  };

  const handleHourRuleChange = (index, key, value) => {
    const updatedHourRules = [...hourRules];
    if (key === 'hour') {
      updatedHourRules[index].timestamp = `${value}:00`;
    } else {
      updatedHourRules[index][key] = value;
    }
    setHourRules(updatedHourRules);
  };

  const handleRemoveHourRule = (index) => {
    const updatedHourRules = [...hourRules];
    updatedHourRules.splice(index, 1);
    setHourRules(updatedHourRules);
  };

  const handleAddSeasonRule = () => {
    if (seasonRules.length < 4) {
      setSeasonRules([...seasonRules, { season: '', type: '+', percent: '' }]);
    }
  };
  
  const handleRemoveSeasonRule = (index) => {
    const updatedSeasonRules = [...seasonRules];
    updatedSeasonRules.splice(index, 1);
    setSeasonRules(updatedSeasonRules);
  };
  
  const handleSeasonRuleChange = (index, key, value) => {
    const updatedSeasonRules = [...seasonRules];
    updatedSeasonRules[index][key] = value;
    setSeasonRules(updatedSeasonRules);
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
                    <div>
                      <label htmlFor="timezone">Time Zone:</label>
                      <select
                        id="timezone"
                        value={timezone}
                        onChange={(e) => setTimezone(e.target.value)}
                      >
                        <option value="EST">EST</option>
                        <option value="PST">PST</option>
                      </select>
                    </div>
                    <div>
                        <h4>Hour Rules</h4>
                        {hourRules.map((rule, index) => (
                            <div key={index}>
                                <label htmlFor={`hour${index}`}>Hour of the Day:</label>
                                <select
                                    id={`hour${index}`}
                                    value={rule.hour}
                                    onChange={(e) => handleHourRuleChange(index, 'hour', e.target.value)}
                                >
                                    <option value="">Select Hour</option>
                                    <option value="1">01:00</option>
                                    <option value="2">02:00</option>
                                    <option value="3">03:00</option>
                                    <option value="4">04:00</option>
                                    <option value="5">05:00</option>
                                    <option value="6">06:00</option>
                                    <option value="7">07:00</option>
                                    <option value="8">08:00</option>
                                    <option value="9">09:00</option>
                                    <option value="10">10:00</option>
                                    <option value="11">11:00</option>
                                    <option value="12">12:00</option>
                                    <option value="13">13:00</option>
                                    <option value="14">14:00</option>
                                    <option value="15">15:00</option>
                                    <option value="16">16:00</option>
                                    <option value="17">17:00</option>
                                    <option value="18">18:00</option>
                                    <option value="19">19:00</option>
                                    <option value="20">20:00</option>
                                    <option value="21">21:00</option>
                                    <option value="22">22:00</option>
                                    <option value="23">23:00</option>
                                    <option value="24">24:00</option>
                                </select>
                                <label htmlFor={`type${index}`}>Type:</label>
                                <select
                                    id={`type${index}`}
                                    value={rule.type}
                                    onChange={(e) => handleHourRuleChange(index, 'type', e.target.value)}
                                >
                                    <option value="+">+</option>
                                    <option value="-">-</option>
                                </select>
                                <label htmlFor={`percent${index}`}>Percent (%):</label>
                                <input
                                    type="text"
                                    id={`percent${index}`}
                                    value={rule.percent}
                                    onChange={(e) => handleHourRuleChange(index, 'percent', e.target.value)}
                                />
                                <button onClick={(e) => { e.stopPropagation(); handleRemoveHourRule(index); }}>Remove Rule</button>
                            </div>
                        ))}
                        {hourRules.length < 24 && (
                            <button onClick={handleAddHourRule}>Add Hour Rule</button>
                        )}
                    </div>
                </div>
            )}
            {ruleType === 'Seasonality' && (
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
                  <label htmlFor="duration">Duration (years):</label>
                  <input
                    type="text"
                    id="duration"
                    value={duration}
                    onChange={(e) => setDuration(e.target.value)}
                  />
                </div>
                <div>
                  <h4>Season Rules</h4>
                  {seasonRules.map((rule, index) => (
                    <div key={index}>
                      <p>{rule.season}</p> {/* Static text for season */}
                      <label htmlFor={`type${index}`}>Type:</label>
                      <select
                        id={`type${index}`}
                        value={rule.type}
                        onChange={(e) => handleSeasonRuleChange(index, 'type', e.target.value)}
                      >
                        <option value="+">+</option>
                        <option value="-">-</option>
                      </select>
                      <label htmlFor={`percent${index}`}>Percent (%):</label>
                      <input
                        type="text"
                        id={`percent${index}`}
                        value={rule.percent}
                        onChange={(e) => handleSeasonRuleChange(index, 'percent', e.target.value)}
                      />
                    </div>
                  ))}
                </div>
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