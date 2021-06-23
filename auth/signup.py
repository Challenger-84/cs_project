from flask import Blueprint, request, current_app, url_for, render_template, session, flash, redirect
from werkzeug.security import generate_password_hash

from db_queries import add_user,if_user


signup_blueprint = Blueprint('signup', __name__, template_folder='templates', static_folder='static')

@signup_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    """ The signup page """

    mysql = current_app.config['mysql']

    # If the request method is POST (ie the user clicked a button on the page)
    if request.method == 'POST':
        # Getting the inputs
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_pass = request.form['confirm password']

        conn = mysql.connection

        flash_message = ""
        # Checking if everything is proper
        if not username:
            flash_message = "Username is not filled"
        elif if_user(conn, username):
            flash_message = "Username already exists"
        elif not password:
            flash_message = "Password is not filled"
        elif password != confirm_pass:
            flash_message = "Passwords do not match"
        else:
            # Creating the account is everything is proper

            # Hashing the password before storing it in out database
            password_hash = generate_password_hash(password)

            # Adds the data to the db
            add_user(conn, username, email, password_hash, 'user')

            # Creating the session
            session.permanent = True
            session['username'] = username

            flash('Successfully created the account', 'info')
            conn.close()
            return redirect(url_for('profile'))
        
        if flash_message:
            # If any error in the input we flash a message
            flash(flash_message, 'info')
            conn.close()
            return redirect(url_for('signup.signup'))

    else:
        # If the request method is GET (ie The user opened the webpage)
        return render_template('sign_up.html', 
                homepage_link = url_for('home')
            )