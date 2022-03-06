from flask import (
    Blueprint,
    request,
    current_app,
    url_for,
    render_template,
    session,
    flash,
    redirect,
)
from numpy import sign
from werkzeug.security import generate_password_hash

from utils.db_queries import add_user, if_user
from utils.otp_gen import generate_otp
import utils.mailer as mailer


signup_blueprint = Blueprint(
    "signup", __name__, template_folder="templates", static_folder="static"
)


@signup_blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    """The signup page"""

    mysql = current_app.config["mysql"]

    # If the request method is POST (ie the user clicked a button on the page)
    if request.method == "POST":
        # Getting the inputs
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_pass = request.form["confirm password"]

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

            # Hashing the password before storing it in out database
            password_hash = generate_password_hash(password)

            # Adds the data to the db
            add_user(conn, username, email, password_hash, "user")

            # Creating the session
            session.permanent = True
            session["username"] = username
            session["user_type"] = "user"
            
             # Sending OTP if everything is proper
            OTP = generate_otp()
            session['OTP'] = OTP
            # Sending the OTP 
            subject = 'OTP for signing up'
            body = f'Your OTP for signing up for SSE boutique store is:\n{OTP}'
            mailer.send_mail(email, subject, body) 

            conn.close()
            return redirect(url_for("signup.enterOtp"))

        if flash_message:
            # If any error in the input we flash a message
            flash(flash_message, "info")
            conn.close()
            return redirect(url_for("signup.signup"))

    else:
        # If the request method is GET (ie The user opened the webpage)
        return render_template(
            "sign_up.html",
            homepage_link=url_for("home"),
            login_link=url_for("login.login"),
        )

@signup_blueprint.route("/enterOTP", methods=['GET', 'POST'])
def enterOtp():
    if request.method == 'POST':
        entered_otp = request.form['OTP']
        if entered_otp == session['OTP']:
            flash = 'Successfully Logged In'
            return redirect(url_for('profile'))
        else:
            flash_message = 'Incorrect OTP'
        
        flash(flash_message, "info")

    else:
        return render_template(
            "enterOtp.html",
            homepage_link=url_for("home"),
            login_link=url_for("login.login")
        )