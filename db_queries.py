import mysql.connector as mysql

def add_user(conn: mysql.connection, username, 
                email, password, account_tpye):
    """Adds a new user to the table 'users'"""
    cursor = conn.cursor() 
    query = f'INSERT INTO users (username, email, password, accounttype) VALUES ("{username}", "{email}", "{password}", "{account_tpye}")'
    print(query)
    cursor.execute(query)
    conn.commit()

    print('addded')

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
    print(output)
    return output

def password_auth(conn: mysql.connection, username, password):
    cursor = conn.cursor()
    query = f'SELECT password FROM users WHERE username="{username}"'
    cursor.execute(query)

    output = cursor.fetchone()
    print(output)
    return password == output[0]