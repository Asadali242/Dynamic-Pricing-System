import psycopg2

# Define the connection parameters
DB_HOST = "lula-dynamicpricing-testdb.ca3vbbjlumqp.us-east-1.rds.amazonaws.com"
DB_PORT = 5432
DB_USER = "lulapricingtest"
DB_PASSWORD = "luladbtest"
DB_NAME = "postgres"

def getItemsByCategory(category):
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cur = conn.cursor()
        query = """
            SELECT si.id AS store_item_id, si.name AS store_item_name, si.price AS store_item_price
            FROM storeitems si
            JOIN storeitemcategories sic ON si.id = sic.store_item_id
            JOIN categories c ON sic.category_id = c.id
            WHERE c.name = %s
        """
        cur.execute(query, (category,))
        items = cur.fetchall()
        cur.close()
        conn.close()
        return items
    except psycopg2.Error as e:
        print("Error fetching items:", e)
        return []
    

def getItems(limit=20):
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cur = conn.cursor()
        query = """
            SELECT si.id AS store_item_id, si.name AS store_item_name, si.price AS store_item_price
            FROM storeitems si
            ORDER BY si.name
            LIMIT %s
        """
        cur.execute(query, (limit,))
        items = cur.fetchall()
        cur.close()
        conn.close()
        return items
    except psycopg2.Error as e:
        print("Error fetching items:", e)
        return []

# Example usage:
items = getItemsByCategory('Chicken')
for item in items:
    print(item)


items = getItems()
for item in items:
    print(item)