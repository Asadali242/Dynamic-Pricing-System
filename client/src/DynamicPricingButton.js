import React from 'react';

function DynamicPricingButton({ onClick }) {
    return (
        <button onClick={onClick}>
            Dynamic Pricing
        </button>
    );
}

export default DynamicPricingButton;