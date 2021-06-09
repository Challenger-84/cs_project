from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
   return "Hello World"

@app.route('/login')
def login():
    return 'this is the login page'

@app.route('/signup')
def signup():
    return 'this is the signup page'

if __name__ == '__main__':
   app.run()