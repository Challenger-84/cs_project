from flask import Blueprint, render_template, current_app, session, url_for

from utils.db_queries import get_cart

cartpage_blueprint = Blueprint(
    "cartpage", __name__, template_folder="templates", static_folder="static"
)


@cartpage_blueprint.route("/cartpage")
def cartpage():
    # mysql connection
    mysql = current_app.config["mysql"]
    connection = mysql.connection

    print(session.items(), get_cart(connection, session["username"]))
    return render_template(
        "cartpage.html", cart=get_cart(connection, session["username"]),
        homepage_link = url_for('home')
    )
