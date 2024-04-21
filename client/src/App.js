// Hello World
import logo from './logo.svg';
import './App.css';
import React, { useState } from 'react';
import InventoryButton from './InventoryButton';
import DynamicPricingButton from './DynamicPricingButton';
import InventoryMenu from './InventoryMenu';
import DynamicPricingMenu from './DynamicPricingMenu';

function App() {
  // State to track which menu should be displayed
  const [activeMenu, setActiveMenu] = useState(null);

  const openInventoryMenu = () => setActiveMenu('inventory');
  const openDynamicPricingMenu = () => setActiveMenu('dynamicPricing');

  const closeMenu = () => setActiveMenu(null);

  return (
    <div className="container">
      <div className="sidebar">
        <h1>Lula Dynamic Pricing System</h1>
        <img 
          src="https://static.wixstatic.com/media/70b423_a809613c0ee940fa9a34ac75e3746c42~mv2.png/v1/fit/w_2500,h_1330,al_c/70b423_a809613c0ee940fa9a34ac75e3746c42~mv2.png" 
          alt="Lulu Logo" 
          className="lulu-logo" // Apply the CSS class
        />
        <div className="button-container">
          <InventoryButton onClick={openInventoryMenu} />
          <DynamicPricingButton onClick={openDynamicPricingMenu} />
        </div>
      </div>
      <div className="content">
        {activeMenu === 'inventory' && <InventoryMenu onClose={closeMenu} />}
        {activeMenu === 'dynamicPricing' && <DynamicPricingMenu onClose={closeMenu} />}
      </div>
    </div>
  );
}

export default App;