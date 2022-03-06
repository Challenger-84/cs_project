import mysql.connector as mysql

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


# Dress related DB functions

dress_keys = ['id', 'name', 'description', 'img_url', 'price', 'stock', 'metadata']
def getDress(conn: mysql.connection, id):
    cursor = conn.cursor()
    query = f"SELECT * FROM dress WHERE dressid={id}"
    cursor.execute(query)
    return dict(zip(dress_keys, cursor.fetchone()))


def searchDress(conn: mysql.connection, search_term):
    cursor = conn.cursor()
    query = f"SELECT * FROM dress WHERE name LIKE '%{search_term}%'"
    cursor.execute(query)

    return cursor.fetchall()


def add_dress(conn: mysql.connection, name, description, img_url, price, stock, metadata):
    cursor = conn.cursor()
    query = f'INSERT INTO dress (name,description,img_url,price,stock, metadata) VALUES("{name}","{description}","{img_url}","{price}","{stock}", "{metadata})'

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

def add_to_cart(conn: mysql.connection, userid, dressid, metadata):
    cursor = conn.cursor()
    query = f'INSERT INTO cart (customer_id, dressid, metadata) VALUES("{userid}","{dressid}","{metadata}")'

    cursor.execute(query)
    conn.commit()
    
