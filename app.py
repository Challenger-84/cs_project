from flask import Flask,render_template, url_for, redirect, request, session, flash
from flask_mysql_connector import MySQL
from werkzeug.security import generate_password_hash, check_password_hash


from db_queries import add_user, view_all_users, if_user, password_hash_returner

app = Flask(__name__)

# Setting up config var for mysql
app.config['MYSQL_USER'] = 'sql6419760'
app.config['MYSQL_HOST'] = 'sql6.freesqldatabase.com'
app.config['MYSQL_DATABASE'] = 'sql6419760'
app.config['MYSQL_PASSWORD'] = 'Y7xYSrHExL'
app.config['MYSQL_PORT'] = '3306'
mysql = MySQL(app)

# seckret key dont leak :)
app.secret_key = "Veryvery secret key :). ha"

@app.route('/')
def home():
    if 'username' in session:
        is_loggedin = True
    else:
        is_loggedin = False

    return render_template('index.html', 
            login_link = url_for('login'),
            signup_link = url_for('signup'), 
            logout_link = url_for('logout'),
            is_loggedin = is_loggedin
        )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connection
        if if_user(conn, username):
            password_hash = password_hash_returner(conn, username, password)
            print(password_hash, password)
            if check_password_hash(password_hash, password):
                session['username'] = username
                flash('Successfully logged in!', 'info')
                return redirect(url_for('profile'))
            else:
                flash('Please check your username and password.', 'info')
                return redirect(url_for('login'))
        else:
            flash("Account doesn't exist", 'info')
            return render_template('login.html',
                    homepage_link = url_for('home')
                )
    else:
        if 'username' in session:
            flash('Already logged in.', 'info')
            return redirect(url_for('profile'))
        else:
            return render_template('login.html',
                    homepage_link = url_for('home')
                )

@app.route('/signup', methods=['GET', 'POST'])
def signup():
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

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
        flash('Logged out.')
        return redirect(url_for('home'))
    else:
        flash('Not logged in.')
        return redirect(url_for('home'))

@app.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        return render_template('profile.html', user=username, homepage_link=url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/dbtest')
def dbtest():
    conn = mysql.connection 
    
    output = view_all_users(conn)

    return str(output)

if __name__ == '__main__':
   app.run(debug=True)