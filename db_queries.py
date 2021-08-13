import mysql.connector as mysql

def add_user(conn: mysql.connection, username, 
                email, password, account_tpye):
    """Adds a new user to the table 'users'"""
    cursor = conn.cursor() 
    query = f'INSERT INTO users (username, email, password, account_type) VALUES ("{username}", "{email}", "{password}", "{account_tpye}")'
    cursor.execute(query)
    conn.commit()


def view_all_users(conn: mysql.connection):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users;')
    
    output = cursor.fetchall()
    return output

def if_user(conn: mysql.connection, username):
    cursor = conn.cursor()
    query= f'SELECT * FROM users WHERE username="{username}"'
    cursor.execute(query)
    
    output = cursor.fetchone()
    return output

def login_info_returner(conn: mysql.connection, username):
    cursor = conn.cursor(buffered=True)
    query = f'SELECT password, account_type FROM users WHERE username="{username}"'
    cursor.execute(query)

    output = cursor.fetchone()
    return output

def add_dress(conn:mysql.connection,name,description,img_url, price, stock):
    cursor=conn.cursor()
    query=f'INSERT INTO dress(name,description,img_url,price,stock)VALUES("{name}","{description}","{img_url}","{price}","{stock}")'
    cursor.execute(query)
    conn.commit()

def view_all_dress(conn:mysql.connection):
    cursor=conn.cursor()
    cursor.execute("SELECT * from dress;")

    output=cursor.fetchall()
    return output

def update_user_account(conn:mysql.connection, userid, new_account_type):
    cursor=conn.cursor()
    query= f'UPDATE users SET account_type="{new_account_type}" where userid="{userid}";'
    cursor.execute(query)
    conn.commit()

def deleteuser(conn:mysql.connection, id):
    cursor = conn.cursor()
    query = f'DELETE FROM users WHERE userid={id}'
    cursor.execute(query)
    conn.commit()

def getDress(conn: mysql.connection, id):
    cursor = conn.cursor()
    query = f"SELECT * FROM dress WHERE dressid={id}"
    cursor.execute(query)

    return cursor.fetchone()