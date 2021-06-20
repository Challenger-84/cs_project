from flask import Blueprint, request, current_app, url_for, render_template, session, flash, redirect
from werkzeug.security import generate_password_hash

from db_queries import add_user,if_user


signup_blueprint = Blueprint('signup', __name__, template_folder='templates', static_folder='static')

@signup_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    mysql = current_app.config['mysql']

    if request.method == 'POST':
        print('test')
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_pass = request.form['confirm password']

        conn = mysql.connection
        if not if_user(conn, username):
            if password == confirm_pass:
                password_hash = generate_password_hash(password)
                print(password_hash)
                add_user(conn, username, email, password_hash, 'user')

                session.permanent = True
                session['username'] = username

                flash('Successfully created the account', 'info')
                return redirect(url_for('profile'))
            else:
                flash('Passwords do not match')
                return redirect(url_for('signup'))
        else:
            flash('Username already exists', 'info')
            return redirect(url_for('signup'))

    else:
        return render_template('sign_up.html', 
                homepage_link = url_for('home')
            )