from flask import (
    Blueprint,
    render_template,
    current_app,
    session,
    url_for,
    request,
    redirect,
)

from utils.db_queries import get_cart, get_userinfo, del_cart
import utils.mailer as mailer

cartpage_blueprint = Blueprint(
    "cartpage", __name__, template_folder="templates", static_folder="static"
)


@cartpage_blueprint.route("/cartpage", methods=["GET", "POST"])
def cartpage():
    # mysql connection
    mysql = current_app.config["mysql"]
    connection = mysql.connection

    if request.method == "POST":
        user_info = get_userinfo(connection, session["username"])
        user_mail = user_info[2]
        subject = "Receipt for your last purchase"
        body = f'Here is the receipt for your purchase: {get_cart(connection, session["username"])}'
        mailer.send_mail(user_mail, subject, body)

        # Removing items from cart
        del_cart(connection, session['username'])

        return redirect(url_for("home"))
    else:
        if ("username" in session) and (session["username"] != ""):
            return render_template(
                "cartpage.html",
                cart=get_cart(connection, session["username"]),
                homepage_link=url_for("home"),
            )
        else:
            return redirect(url_for("login.login"))


@cartpage_blueprint.route("/checkout", methods=["GET", "POST"])
def checkout():
    # mysql connection
    mysql = current_app.config["mysql"]
    connection = mysql.connection

    if request.method == "POST":
        print(session.keys())
        user_mail = get_userinfo(connection, session["username"])
        subject = "Receipt for your last purchase"
        body = f'Here is the receipt for your purchase: {get_cart(connection, session["username"])}'
        print(user_mail, subject, body)
        mailer.send_mail(user_mail, subject, body)

        return redirect(url_for("home"))

    else:
        return render_template(
            "checkout.html",
            cart=get_cart(connection, session["username"]),
            homepage_link=url_for("home"),
        )
