import os
import json

from flask import Flask
from flask import request
from flask import jsonify
from redis import Redis
import psycopg2

from utils import validate_string_as_number

conn = psycopg2.connect(
    host="database",
    database="postgres",
    user="postgres",
)


cur = conn.cursor()
app = Flask(__name__)
redis = Redis(host="redis", port=6379)


@app.route("/products/<_id>/buy")
def buy(_id):
    cur.execute(
        "UPDATE products SET quantity = quantity - 1 WHERE id = (%s);", (_id,))
    affected_row_count = cur.rowcount
    conn.commit()
    user_email = request.args.get("email", None)
    if affected_row_count == 1:
        redis.incr(_id)
        
        if user_email:
            redis.lpush(user_email, _id)

            # To test in in redis container,
            # redis-cli
            # LLEN "example@mail.com"
            # LPOP "example@mail.com"

        resp = {
            "action": f"You bought item with id:{_id}.",
            "summary": f"This item has been bought {redis.get(_id)} times.",
        }
        return jsonify(resp), 200
    else:
        resp = {
            "action": f"You tried to buy item with id:{_id}.",
            "error": f"This item is not found",
        }
        return jsonify(resp), 400  # Could also use 404


@app.route("/products")
def list_products():
    limit = request.args.get("limit", None)
    offset = request.args.get("offset", None)

    if not validate_string_as_number(limit):
        return jsonify({"error": "bad value for limit"}), 400

    if not validate_string_as_number(offset):
        return jsonify({"error": "bad value for offset"}), 400

    statement = (
        "select id,image_src,price,title,quantity from products order by date_added"
    )

    if offset is not None:
        statement += f" offset {offset}"

    if limit is not None:
        statement += f" limit {limit}"

    statement += ";"

    cur.execute(statement)
    data = cur.fetchall()

    response = [
        {
            "id": row[0],
            "image_src": row[1],
            "price": row[2],
            "title": row[3],
            "quantity": row[4],
        }
        for row in data
    ]

    return jsonify(response)


@app.route("/products/", methods=["POST"])
def insert_product():
    data = json.loads(request.data)
    if "quantity" not in data.keys():
        cur.execute(
            "INSERT INTO products (image_src, title, price)" "VALUES (%s, %s, %s)",
            (
                data["image_src"],
                data["title"],
                data["price"],
            ),
        )
    else:
        cur.execute(
            "INSERT INTO products (image_src, title, price, quantity)"
            "VALUES (%s, %s, %s, %s)",
            (
                data["image_src"],
                data["title"],
                data["price"],
                data["quantity"],
            ),
        )

    conn.commit()
    return jsonify(201)


@app.route("/products/<_id>", methods=["DELETE"])
def delete_product(_id):
    cur.execute("DELETE FROM products WHERE id=%s", (_id,))
    if cur.rowcount > 0:
        msg = {"message": f"Deleted {cur.rowcount} rows"}
        status_code = 200
    else:
        msg = {"error": f"Product with id {_id} not found"}
        status_code = 400  # again can be also 404 if you want to
    conn.commit()
    return jsonify(msg), status_code


@app.route("/products/<_id>", methods=["GET"])
def get_product(_id):
    cur.execute(
        "SELECT id,image_src,price,title,quantity FROM products WHERE id=%s", (
            _id,)
    )
    if cur.rowcount == 0:
        msg = {"error": f"Product with id {_id} not found"}
        status_code = 400  # again can be also 404 if you want to
        return jsonify(msg), status_code

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


@app.route("/products/<_id>", methods=["PUT"])
def update_product(_id):
    data = json.loads(request.data)
    s = ""
    for k in data.keys():
        s += f"{k}=(%s),"
    s = s[:-1]

    values = list(data.values())
    values.append(_id)

    cur.execute("UPDATE products SET " + s + " WHERE id = (%s);", (values))
    conn.commit()
    return jsonify(200)

@app.route("/users/", methods=["POST"])
def insert_user():
    data = json.loads(request.data)
    cur.execute(
        "INSERT INTO users (first_name, last_name, address, email, phone_number)"
        "VALUES (%s, %s, %s, %s, %s)",
        (
            data["first_name"],
            data["last_name"],
            data["address"],
            data["email"],
            data["phone_number"],
        ),
    )

    conn.commit()
    return jsonify(201)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ["PORT"], debug=True)
