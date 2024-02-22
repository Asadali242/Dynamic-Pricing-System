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
        <h1>Lula Dynamic Pricing Development Testing</h1>
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