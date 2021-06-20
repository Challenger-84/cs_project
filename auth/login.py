from flask import Blueprint , request, session, flash, redirect, render_template, url_for, current_app
from flask_mysql_connector import MySQL
from werkzeug.security import check_password_hash

from db_queries import if_user, password_hash_returner


login_blueprint = Blueprint('login', __name__, template_folder="templates", static_folder="static")


@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    mysql = current_app.config['mysql']

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connection
        if if_user(conn, username):
            password_hash = password_hash_returner(conn, username, password)
            print(password_hash, password)
            if check_password_hash(password_hash, password):
                session.permanent = True
                session['username'] = username
                flash('Successfully logged in!', 'info')
                return redirect(url_for('profile'))
            else:
                flash('Please check your username and password.', 'info')
                return redirect(url_for('login'))
        else:
            flash("Account doesn't exist", 'info')
            return redirect(url_for('login'))
    else:
        if 'username' in session:
            flash('Already logged in.', 'info')
            return redirect(url_for('profile'))
        else:
            return render_template('login.html',
                    homepage_link = url_for('home')
                )

@login_blueprint.route('/logout')
def logout():
    print(session)
    if 'username' in session:
        session.pop('username', None)
        flash('Logged out.')
        return redirect(url_for('home'))
    else:
        flash('Not logged in.')
        return redirect(url_for('home'))