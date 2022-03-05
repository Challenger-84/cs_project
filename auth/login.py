from auth.signup import signup
from flask import (
    Blueprint,
    request,
    session,
    flash,
    redirect,
    render_template,
    url_for,
    current_app,
)
from flask_mysql_connector import MySQL
from werkzeug.security import check_password_hash

from utils.db_queries import if_user, login_info_returner


login_blueprint = Blueprint(
    "login",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/auth/static",
)


@login_blueprint.route("/login", methods=["GET", "POST"])
def login():
    """The Login Page"""

    mysql = current_app.config["mysql"]

    # If the request method is POST (ie the user clicked a button on the page)
    if request.method == "POST":

        # Getting the inputs
        username = request.form["username"]
        password = request.form["password"]

        conn = mysql.connection

        login_info = login_info_returner(conn, username)
        print(login_info)
        # Checking if the user exists in our database
        if if_user(conn, username):
            password_hash = login_info[0]  # Password hash
            # Checking if the password is correct
            if check_password_hash(password_hash, password):
                # Logging in the user if the checks are passed
                session.permanent = True
                session["username"] = username
                session["user_type"] = login_info[1]  # account type
                print(session["user_type"])
                flash("Successfully logged in!", "info")
                conn.close()
                return redirect(url_for("profile"))
            else:
                # Flashing a message if there is a error in the input
                flash("Please check your username and password.", "info")
                conn.close()
                return redirect(url_for("login.login"))
        else:
            # Flashing a message is there is no account with the inputed username
            flash("Account doesn't exist", "info")
            conn.close()
            return redirect(url_for("login.login"))

    # If the request method is GET (ie The user opened the webpage)
    else:
        # If user is already logged in we redirect to the Profile page
        if "username" in session:
            flash("Already logged in.", "info")
            return redirect(url_for("profile"))
        else:
            print(url_for("signup.signup"))
            # If not we show the login page
            return render_template(
                "login.html",
                homepage_link=url_for("root"),
                signup_link=url_for("signup.signup"),
            )


@login_blueprint.route("/logout")
def logout():
    """The logout page"""
    # Checking if user is logged in
    if "username" in session:
        # Deleting the session data
        session.pop("username", None)
        flash("Logged out.")
        return redirect(url_for("root"))
    else:
        # If the user tries to logout without being logged in we flash a message
        flash("Not logged in.")
        return redirect(url_for("root"))
