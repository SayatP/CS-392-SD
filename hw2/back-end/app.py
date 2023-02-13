import os
import json

from flask import Flask
from flask import request
from flask import jsonify
from redis import Redis

import psycopg2

conn = psycopg2.connect(
    host="database",
    database="postgres",
    user="postgres",
)


cur = conn.cursor()
app = Flask(__name__)
redis = Redis(host='redis', port=6379)


@app.route('/products/buy')
def buy():
    _id = request.args['id']
    redis.incr(_id)
    resp = {
        "action": f'Someone bought item with {_id}!',
        "summary": f"This has been bought {redis.get(_id)} times!", }
    cur.execute(
        "UPDATE products SET quantity = quantity - 1 WHERE id = (%s);",
        (_id,)
    )
    conn.commit()
    return jsonify(resp)


@app.route('/products/all')
def list_products():
    cur.execute("select id,image_src,price,title,quantity from products order by date_added;")
    data = cur.fetchall()

    response = [

        {
            "id": row[0],
            "image_src": row[1],
            "price": row[2],
            "title": row[3],
            "quantity": row[4],
        }

        for row in data]

    return jsonify(response)


@app.route('/products/', methods=["POST"])
def insert_product():
    data = json.loads(request.data)
    if "quantity" not in data.keys():
        cur.execute('INSERT INTO products (image_src, title, price)'
                    'VALUES (%s, %s, %s)',
                    (data['image_src'],
                        data['title'],
                        data['price'],
                     )
                    )
    else:
        cur.execute('INSERT INTO products (image_src, title, price, quantity)'
                    'VALUES (%s, %s, %s, %s)',
                    (data['image_src'],
                        data['title'],
                        data['price'],
                        data['quantity'],
                     )
                    )

    conn.commit()
    return jsonify(201)


@app.route('/products/<_id>', methods=["DELETE"])
def delete_product(_id):
    cur.execute('DELETE FROM products WHERE id=%s', (_id,))
    conn.commit()
    return jsonify(200)


@app.route('/products/<_id>', methods=["GET"])
def get_product(_id):
    cur.execute(
        'SELECT id,image_src,price,title,quantity FROM products WHERE id=%s', (_id,))
    row = cur.fetchone()
    return jsonify(
        {
            "id": row[0],
            "image_src": row[1],
            "price": row[2],
            "title": row[3],
            "quantity": row[4],
        }
    )


@app.route('/products/<_id>', methods=["PUT"])
def update_product(_id):
    data = json.loads(request.data)
    s = ""
    for k in data.keys():
        s += f"{k}=(%s),"
    s = s[:-1]

    values = list(data.values())
    values.append(_id)

    cur.execute(
        "UPDATE products SET " + s + " WHERE id = (%s);",
        (values)
    )
    conn.commit()
    return jsonify(200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ["PORT"], debug=True)
