from flask import Flask,render_template, url_for, redirect, request, session
from flask_mysql_connector import MySQL
from werkzeug.utils import redirect

app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DATABASE'] = 'sys'
mysql = MySQL(app)

app.secret_key = "Veryvery secret key :). ha"

@app.route('/')
def home():  
   return render_template('index.html', 
            login_link = url_for('login'),
            signup_link = url_for('signup')
        )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('profile'))
    else:
        return render_template('login.html',
                homepage_link = url_for('home')
            )

@app.route('/signup')
def signup():
    return render_template('sign_up.html', 
            homepage_link = url_for('home')
        )

@app.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        return render_template('profile.html', user=username, homepage_link=url_for('home'))
    else:
        return redirect('login')


if __name__ == '__main__':
   app.run(debug=True)