const { Client } = require('pg');

const client = new Client({
    host:"lula-dynamicpricing-testdb.ca3vbbjlumqp.us-east-1.rds.amazonaws.com",
    port:5432,
    user:"lulapricingtest",
    password:"luladbtest",
    database:"postgres"
})

client.connect();


/*client.query('select * From StoreItems', (err, result) => {
    if(!err){
        console.log(result.rows);
    }
    client.end;
})*/


function getItemsByCategory(category, callback) {
    const query = `
        SELECT si.id AS store_item_id, si.name AS store_item_name, si.price AS store_item_price
        FROM storeitems si
        JOIN storeitemcategories sic ON si.id = sic.store_item_id
        JOIN categories c ON sic.category_id = c.id
        WHERE c.name = $1`;

    client.query(query, [category], (err, result) => {
        if (!err) {
            console.log(result.rows);
            callback(null, result.rows);
        } else {
            console.error('Error executing query:', err);
            callback(err, null);
        }
        client.end();
    });
}

// Example usage:
getItemsByCategory('Ice Cream', (err, items) => {
    if (!err) {
        console.log(items);
    } else {
        console.error('Error:', err);
    }
});