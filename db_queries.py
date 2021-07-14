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

def password_hash_returner(conn: mysql.connection, username, password):
    cursor = conn.cursor(buffered=True)
    query = f'SELECT password FROM users WHERE username="{username}"'
    cursor.execute(query)

    output = cursor.fetchone()
    return output[0]

def add_values(conn:mysql.connection,name,img_url, price, stock):
    cursor=conn.cursor()
    query=f'INSERT INTO dress(name,description,img_url,price,stock)VALUES({name}","{img_url}","{price}","{stock}")'
    cursor.execute(query)
    conn.commit()

def see_all_dress(conn:mysql.connection):
    cursor=conn.cursor()
    cursor.execute("SELECT * from dress;")

    output=cursor.fetchall()
    return output

def update_user_account(conn:mysql.connection,username,password):
    cursor=conn.cursor()
    query='UPDATE users SET account_type="{username}","{password}")where userid={userid} and username={username})'
    cursor.execute(query)
    conn.commit()


    
