import React from 'react';

const Item = ({ item, index }) => (
    <div key={index} className="item-container">
      <div className="item-image">
        {item[1] === 'Armour Chicken Vienna Bites' && (
          <img src="https://www.instacart.com/image-server/932x932/filters:fill(FFF,true):format(webp)/www.instacart.com/assets/domains/product-image/file/large_1e786f7c-eb99-4f99-b1da-d69b44846d92.jpeg" alt="Armour Chicken Vienna Bites" />
        )}
        {item[1] === "Ben & Jerry's Americone Dream" && (
          <img src="https://shop.benjerry.com/cdn/shop/products/36796_US_IC_Americone-Dream_473ml_FOP-1000x1000-e30c47ce-d108-45d9-a0da-fbb10bb410c1.png?v=1677670266" alt="Ben & Jerry's Americone Dream" />
        )}
        {item[1] === "Ben & Jerry's Everthing But The..." && (
          <img src="https://i5.walmartimages.com/seo/Ben-Jerry-s-Everything-But-The-Chocolate-and-Vanilla-Ice-Cream-16-oz_eea39013-9dbc-4f2f-9709-b101fa8cc296.9e2adfd57638c6888e33ad1b5f7ac3a3.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF" />
        )}
        {item[1] === "Ben & Jerry's Phish Food" && (
          <img src="https://images.heb.com/is/image/HEBGrocery/000403020-1" alt="Ben & Jerry's Phish Food" />
        )}
        {item[1] === "BUFFALO STYLE CHICKEN STRIPS" && (
          <img src="https://i5.walmartimages.com/seo/Tyson-Fully-Cooked-Buffalo-Style-Chicken-Strips-1-56-lb-Bag-Frozen_123090ff-ef92-4797-93fb-fc71297b9291.a27f4db6c3c67ebd25b3b95928fe26dd.jpeg" alt="BUFFALO STYLE CHICKEN STRIPS" />
        )}
        {item[1] === "Coffee" && (
          <img src="https://www.puffco.com/cdn/shop/products/Cupsy_Front_Facing_grande.png?v=1680818865" alt="Coffee" />
        )}
        {item[1] === "Fountain Drink" && (
          <img src="https://munnchiezdetstyle.com/cdn/shop/products/1E25CC74-A7AE-458D-A370-0869405333D4.jpg?v=1659288661" alt="Fountain Drink" />
        )}
        {item[1] === "Friendly's Coffee Ice Cream" && (
          <img src="https://bk.brooklynfare.com/cdn/shop/products/2983900522.jpg?v=1674124215" alt="Friendly's Coffee Ice Cream" />
        )}
        {item[1] === "GRILLED CARVED CHICKEN BREAST" && (
          <img src="https://www.perdue.com/product-images/81221_640_81221_FV.jpg" alt="GRILLED CARVED CHICKEN BREAST" />
        )}
        {item[1] === "KKC Chicken Sandwich" && (
          <img src="https://assets1.csnews.com/files/s3fs-public/styles/hero/public/2024-01/krsipy_krunchy_cajun_chicken_sandwich_500x281.jpg?VersionId=guY.iiCQS.pchbTv0WEFHa0LrOxBTL8H&itok=6izejvXA" alt="KKC Chicken Sandwich" />
        )}
        {item[1] === "Maple Valley Ice Cream Black Raspberry Chocolate Chunk" && (
          <img src="https://images.freshop.com/00857743002552/e5223fd626cf93ec02e534b4082b97b1_large.png" alt="Maple Valley Ice Cream Black Raspberry Chocolate Chunk" />
        )}
        {item[1] === "Nissy Cup Noodles,Spicy Chile Chicken" && (
          <img src="https://images.gopuff.com/blob/gopuffcatalogstorageprod/catalog-images-container/resize/cf/version=1_2,format=auto,fit=scale-down,width=800,height=800/d99648bd-8cad-4874-b6f1-2ad4eb1f8026.png" alt="Nissy Cup Noodles,Spicy Chile Chicken" />
        )}
        {item[1] === "Red Bull Sugar Free Energy Drink" && (
          <img src="https://m.media-amazon.com/images/I/513sfVLpFvL.jpg" alt="Red Bull Sugar Free Energy Drink" />
        )}
        {item[1] === "Rockstar Pure Zero Fruit Punch Energy Drink" && (
          <img src="https://www.datocms-assets.com/74813/1673641319-rockstar_single_can_purezero_fruit_punch.png" alt="Rockstar Pure Zero Fruit Punch Energy Drink" />
        )}
        {item[1] === "Ruffles Queso Cheese Potato Chips" && (
          <img src="https://www.ruffles.com/sites/ruffles.com/files/2024-02/Queso%202024.png" alt="Ruffles Queso Cheese Potato Chips" />
        )}
        {item[1] === "Smartfood White Cheddar Popcorn" && (
          <img src="https://i5.walmartimages.com/seo/Smartfood-White-Cheddar-Popcorn-6-75-oz-Bag_994bc3b2-b818-45a6-935a-11c3e5664868.b08c2f8be8b5bd73ec493fad5e613fdf.jpeg" alt="Smartfood White Cheddar Popcorn" />
        )}
        {item[1] === "Snyder's Of Hanover Mini Pretzels" && (
          <img src="https://www.simpalosnacks.com/cdn/shop/products/SnydersOfHanover_MiniPretzels_1024x1024.jpg?v=1571439580" alt="Snyder's Of Hanover Mini Pretzels" />
        )}
        {item[1] === "Snyder's Pretzel Pieces Honey Mustard & Onion" && (
          <img src="https://i5.walmartimages.com/seo/Snyder-s-of-Hanover-Pretzel-Pieces-Honey-Mustard-Onion-12-oz_3688a400-c1a5-420d-94fc-cf66b4a918b1.e7bfca28733bca999ed7762e2f64c5e2.jpeg" alt="Snyder's Pretzel Pieces Honey Mustard & Onion" />
        )}
        {item[1] === "TIC TAC BIG PK FRESHMINT" && (
          <img src="https://i5.walmartimages.com/seo/Tic-Tac-1-Oz-Freshmint-Mints-Big-Pack-112090-Pack-of-12-112090-971278_fc36f6a3-a588-4e25-a44e-4d21a0ad1693.29fa1d573fd6633f03f9a2f706759648.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF" alt="TIC TAC BIG PK FRESHMINT" />
        )}
        {item[1] === "Tootsie Roll Razzles Candy" && (
          <img src="https://i5.walmartimages.com/asr/7f6ae98f-2036-4760-931d-55a958dc146d.d0f1519f7bea043d765db2dfad0bf8b6.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF" alt="Tootsie Roll Razzles Candy" />
        )}
        {item[1] === "Trident Spearmint Gum" && (
          <img src="https://m.media-amazon.com/images/I/81+HlAtInPL.jpg" alt="Trident Spearmint Gum" />
        )}
        {item[1] === "TWIX CARAMEL KING SIZE" && (
          <img src="https://media.chevronextramile.com/uploads/2021/04/26095229/Twix-Caramel-Share.jpg" alt="TWIX CARAMEL KING SIZE" />
        )}
        {item[1] === "Twizzlers Nibs Cherry Licorice Candy Bits" && (
          <img src="https://target.scene7.com/is/image/Target/GUEST_042c7233-931f-4234-bda1-2680cb326513?wid=488&hei=488&fmt=pjpeg" alt="Twizzlers Nibs Cherry Licorice Candy Bits" />
        )}
        {item[1] === "Vitamin Water Electrolyte Enhanced Water" && (
          <img src="https://m.media-amazon.com/images/I/81GTm5K1ZXL._AC_UF894,1000_QL80_.jpg" alt="Vitamin Water Electrolyte Enhanced Water" />
        )}
        {item[1] === "Welch's Mixed Fruit Snacks" && (
          <img src="https://www.kroger.com/product/images/medium/front/0003485602888" alt="Welch's Mixed Fruit Snacks" />
        )}
        {/* Add other image sources similarly */}
      </div>
      <div className="item-details">
      <h3>{item[1]}</h3>
      <p>Price: ${`${item[2].slice(0, 1)}.${item[2].slice(1)}`}</p>
    </div>
  </div>
);

export default Item;