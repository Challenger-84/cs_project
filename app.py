from flask import Flask,render_template, url_for, redirect, session
from flask_mysql_connector import MySQL
import mysql.connector

from datetime import timedelta
import os

# Importing blueprints
from auth.login import login_blueprint
from auth.signup import signup_blueprint
from admin.admin import admin_blueprint

from db_queries import view_all_users

app = Flask(__name__)

# Registering the blueprinta
app.register_blueprint(login_blueprint)
app.register_blueprint(signup_blueprint)
app.register_blueprint(admin_blueprint)

# Setting up config var for mysql
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_HOST'] = "eu-cdbr-west-01.cleardb.com"
print(os.getenv('MYSQL_PASSWORD'))
app.config['MYSQL_DATABASE'] = os.getenv('MYSQL_DB')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
mysql = MySQL(app)

app.config['mysql'] = mysql

# seckret key dont leak :)
app.secret_key = os.getenv('SECRET_KEY')

# Setting how long a permanent session lasts
app.permanent_session_lifetime = timedelta(minutes=10)

# HomePage
@app.route('/')
def home():
    if 'username' in session:
        is_loggedin = True  
    else:
        is_loggedin = False

    return render_template('index.html', 
            login_link = url_for('login.login'),
            signup_link = url_for('signup.signup'), 
            logout_link = url_for('login.logout'),
            profile_link = url_for('profile'),
            admin_link = url_for('admin.admin'),
            is_loggedin = is_loggedin
        )

@app.route('/profile')
def profile():
    """User's Profile page"""

    # Checking if the user is logged in
    if 'username' in session:
        username = session['username']
        return render_template('profile.html', user=username,
                             homepage_link=url_for('home'), 
                             admin_link = url_for('admin.admin'))
    else:
        return redirect(url_for('login.login'))

# Only admins :)
@app.route('/dbtest')
def dbtest():
    conn = mysql.connection
    
    output = view_all_users(conn)

    conn.close()
    return str(output)

if __name__ == '__main__':
   app.run(debug=True)