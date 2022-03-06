from flask import url_for
import json
import mysql.connector as mysql

from utils.img_host import get_file

# User related DB functions
def add_user(conn: mysql.connection, username, email, password, account_tpye):
    """Adds a new user to the table 'users'"""
    cursor = conn.cursor()
    query = f'INSERT INTO users (username, email, password, account_type) VALUES ("{username}", "{email}", "{password}", "{account_tpye}")'
    cursor.execute(query)
    conn.commit()


def view_all_users(conn: mysql.connection):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users;")

    output = cursor.fetchall()
    return output


def if_user(conn: mysql.connection, username):
    cursor = conn.cursor()
    query = f'SELECT * FROM users WHERE username="{username}"'
    cursor.execute(query)

    output = cursor.fetchone()
    return output


def login_info_returner(conn: mysql.connection, username):
    cursor = conn.cursor(buffered=True)
    query = f'SELECT password, account_type FROM users WHERE username="{username}"'
    cursor.execute(query)

    output = cursor.fetchone()
    return output


def update_user_account(conn: mysql.connection, userid, new_account_type):
    cursor = conn.cursor()
    query = (
        f'UPDATE users SET account_type="{new_account_type}" where userid="{userid}";'
    )
    cursor.execute(query)
    conn.commit()


def deleteuser(conn: mysql.connection, id):
    cursor = conn.cursor()
    query = f"DELETE FROM users WHERE userid={id}"
    cursor.execute(query)
    conn.commit()


def get_userinfo(conn: mysql.connection, username):
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username='{username}'"
    cursor.execute(query)

    return cursor.fetchone()


# Dress related DB functions

dress_keys = ["id", "name", "description", "img_url", "price", "stock", "metadata"]


def getDress(conn: mysql.connection, id):
    cursor = conn.cursor()
    query = f"SELECT * FROM dress WHERE dressid={id}"
    cursor.execute(query)
    dress = cursor.fetchone()
    if dress is None:
        return None
    return dict(zip(dress_keys, dress))


def searchDress(conn: mysql.connection, search_term):
    cursor = conn.cursor()
    query = f"SELECT * FROM dress WHERE name LIKE '%{search_term}%'"
    cursor.execute(query)

    return cursor.fetchall()


def add_dress(
    conn: mysql.connection, name, description, img_url, price, stock, metadata
):
    cursor = conn.cursor()
    query = f'INSERT INTO dress (name,description,img_url,price,stock, metadata) VALUES("{name}","{description}","{img_url}","{price}","{stock}", \'{metadata}\')'

    cursor.execute(query)
    conn.commit()


def view_all_dress(conn: mysql.connection):
    cursor = conn.cursor()
    cursor.execute("SELECT * from dress;")

    output = cursor.fetchall()
    return output


def del_dress(conn: mysql.connection, id):
    cursor = conn.cursor()
    query = f"DELETE FROM DRESS WHERE dressid={id}"

    cursor.execute(query)
    conn.commit()


def add_to_cart(conn: mysql.connection, username, dressid, metadata):
    cursor = conn.cursor()
    query = f'INSERT INTO cart (customer_id, dressid, metadata) VALUES((SELECT userid FROM users WHERE username="{username}"),"{dressid}",\'{json.dumps(metadata)}\')'

    cursor.execute(query)
    conn.commit()


cart_keys = ["cart_id", "customer_id", "dress_id", "metadata"]


def get_cart(conn: mysql.connection, username):
    cursor = conn.cursor()
    query = f"SELECT * FROM cart WHERE customer_id=(SELECT userid FROM users WHERE username='{username}') and checked_out=0"
    cursor.execute(query)
    cart = list(map(lambda x: dict(zip(cart_keys, x)), cursor.fetchall()))
    dress_ids = list(map(lambda x: x["dress_id"], cart))
    if len(dress_ids) == 0:
        return []
    print(cart)
    cursor.execute(
        f"SELECT metadata, dressid, img_url,name,price FROM dress WHERE dressid IN ({ (','.join(map(str, dress_ids))) });"
    )
    metadata = {}
    metadatas = cursor.fetchall()
    list(map(lambda x: assign(x, metadata), metadatas))
    for i in range(len(cart)):
        item = cart[i]
        meta = metadata[item["dress_id"]]["metadata"]
        metameta = json.loads(item["metadata"])
        for j in metameta:
            meta[j] = metameta[j]
        cart[i]["metadata"] = meta
        cart[i]["image"] = url_for(
            ".static", filename=get_file(metadata[item["dress_id"]]["image"])
        )
        cart[i]["name"] = metadata[item["dress_id"]]["name"]
        cart[i]["price"] = metadata[item["dress_id"]]["price"]

    return cart


def del_cart(conn: mysql.connection, username, delete=False):
    cursor = conn.cursor()
    cursor.execute(f'SELECT userid from users WHERE username="{username}"')
    userid = int(cursor.fetchone()[0])

    if delete:
        cursor.execute(f"DELETE FROM cart WHERE customer_id={userid} AND checked_out=0")
        conn.commit()
    else:
        cursor.execute(f"UPDATE cart SET checked_out=1 WHERE customer_id={userid}")
        conn.commit()


def assign(x, metadata):
    metadata[x[1]] = {
        "metadata": json.loads(x[0]),
        "dressid": x[1],
        "image": x[2],
        "name": x[3],
        "price": x[4],
    }
