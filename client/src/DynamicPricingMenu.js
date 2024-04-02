import React from 'react';

function DynamicPricingMenu() {
  return (
    <div className="dashboard">
      <h2>Dashboard</h2>
      <p>Metrics Coming Soon</p>
      <div className="pricing-menu">
        <h3>Dynamic Pricing</h3>
        <p>This is where you see sales history of enrolled products, currently enrolled products, etc.</p>
        {/* You can add more content specific to the Dynamic Pricing menu */}
      </div>
    </div>
  );
}

export default DynamicPricingMenu;
