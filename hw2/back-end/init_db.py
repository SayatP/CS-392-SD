import psycopg2

conn = psycopg2.connect(
    host="database",
    database="postgres",
    user="postgres",
)
cur = conn.cursor()

# cur.execute('DROP TABLE IF EXISTS products;')
# cur.execute('CREATE TABLE products (id serial PRIMARY KEY,'
#     'image_src varchar (256)'
#     'image_caption varchar (512)'
#     'price decimal(12,2)'
#     'date_added date DEFAULT CURRENT_TIMESTAMP);'
# )

cur.execute(
    "INSERT INTO products (image_src, title, price)" "VALUES (%s, %s, %s)",
    (
        "./static/cb.jpg",
        "Chess board.!",
        26,
    ),
)
cur.execute(
    "INSERT INTO products (image_src, title, price)" "VALUES (%s, %s, %s)",
    (
        "./static/shoes.jpg",
        "Shoes.",
        64,
    ),
)

conn.commit()
cur.close()
conn.close()
