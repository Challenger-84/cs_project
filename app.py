from flask import Flask,render_template, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'freedb.tech'
app.config['MYSQL_USER'] = 'freedbtech_Eshwar'
app.config['MYSQL_PASSWORD'] = 'csproject'
app.config['MYSQL_DB'] = 'freedbtech_CsProject'


@app.route('/')
def home():  
   return render_template('index.html', login_link=url_for('login'), signup_link = url_for('signup') )

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('sign_up.html')

if __name__ == '__main__':
   app.run(debug=True)