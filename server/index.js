const { Client } = require('pg');

const client = new Client({
    host:"lula-dynamicpricing-testdb.ca3vbbjlumqp.us-east-1.rds.amazonaws.com",
    port:5432,
    user:"lulapricingtest",
    password:"luladbtest",
    database:"postgres"
})

client.connect();

client.query('select * From demo_table', (err, result) => {
    if(!err){
        console.log(result.rows);
    }
    client.end;
})