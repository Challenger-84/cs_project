""" Imports """
from flask import Flask,render_template, url_for, redirect, session, request
from flask_mysql_connector import MySQL
import mysql.connector

from datetime import timedelta
import os

from utils.db_queries import view_all_dress, searchDress
from utils.img_host import get_file

# Importing blueprints
from auth.login import login_blueprint
from auth.signup import signup_blueprint
from admin.admin import admin_blueprint
from dress_page.dresspage import dresspage_blueprint
from checkout.cartpage import cartpage_blueprint
""" Imports Done """

app = Flask(__name__)

# Registering the blueprinta
app.register_blueprint(login_blueprint)
app.register_blueprint(signup_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(dresspage_blueprint)
app.register_blueprint(cartpage_blueprint)

# Setting up config var for mysql
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_HOST'] = "eu-cdbr-west-01.cleardb.com"
app.config['MYSQL_DATABASE'] = os.getenv('MYSQL_DB')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
mysql = MySQL(app)

app.config['mysql'] = mysql

app.secret_key = os.getenv('SECRET_KEY')

# Setting how long a permanent session lasts
app.permanent_session_lifetime = timedelta(minutes=10)

@app.route('/')
def root():
    return redirect(url_for('home' , searchterm='#!#!23L#'))

# HomePage
@app.route('/<searchterm>')
def home(searchterm):
    # Checking user type
    if 'username' in session:
        is_loggedin = True
    else:
        is_loggedin = False

    if 'user_type' in session:
        is_admin = session['user_type'] == 'admin'
    else:
        is_admin = False
        session['user_type'] = 'user'

    mysql = app.config['mysql']
    conn = mysql.connection

    if searchterm != '#!#!23L#':
        # Getting result from DB
        mysql = app.config['mysql']
        conn = mysql.connection
        dresses = searchDress(conn, searchterm)
    else:
        dresses = view_all_dress(conn)
    
    new_dresses = []

    # Displaying dresses in main page
    for dress in dresses:
        dress = list(dress)
        dress[3] = get_file(dress[3])
        dress[3] = url_for('.static', filename=dress[3])
        new_dresses.append(dress)

    return render_template('index.html', 
            login_link = url_for('login.login'),
            signup_link = url_for('signup.signup'), 
            logout_link = url_for('login.logout'),
            profile_link = url_for('profile'),
            admin_link = url_for('admin.admin'),
            cartpage_link = url_for('cartpage.cartpage'),
            is_loggedin = is_loggedin,
            is_admin = is_admin,
            dresses = new_dresses
        )

@app.route('/profile')
def profile():
    """User's Profile page"""

    # Checking if the user is logged in
    if 'username' in session:
        username = session['username']

        if 'user_type' in session:
            is_admin = session['user_type'] == 'admin'
        else:
            is_admin = False

        return render_template('profile.html', user=username,
                             homepage_link=url_for('root'), 
                             admin_link = url_for('admin.admin'), 
                             logout_link = url_for('login.logout'),
                             isadmin = is_admin)
    else:
        return redirect(url_for('login.login'))

@app.route('/searchresult/', methods=['GET', 'POST'])
def search():
    """ The page which the user will be redirected to when searching """

    if request.method == 'POST':
        search_term = request.form['Search']
        return redirect(url_for('home', searchterm=search_term))    
    
    else:
        return redirect(url_for('home', searchterm='#!#!23L#'))

if __name__ == '__main__':
   app.run(debug=True)