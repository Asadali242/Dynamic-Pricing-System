import React from 'react';

function InventoryButton({ onClick }) {
    return (
        <button onClick={onClick}>
            Inventory
        </button>
    );
}

export default InventoryButton;