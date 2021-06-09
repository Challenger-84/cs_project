from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
   return "Hello World"

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('sign_up.html')

if __name__ == '__main__':
   app.run()