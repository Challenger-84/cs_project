from flask import Blueprint, flash, render_template, current_app, request, session, url_for
from itsdangerous import json

from utils.db_queries import add_to_cart, getDress
from utils.img_host import get_file

dresspage_blueprint = Blueprint(
    "dresspage", __name__, template_folder="templates", static_folder="static"
)


@dresspage_blueprint.route("/dresspage/<dressid>", methods=["GET", "POST"])
def dresspage(dressid):
    mysql = current_app.config["mysql"]
    connection = mysql.connection
    if request.method == "POST":
        if "username" not in session.keys():
            flash("You need to login first")
        else:
            metadata = request.form
            add_to_cart(connection, session["username"], dressid, metadata)
    dress_info = getDress(connection, dressid)

    img_path = dress_info["img_url"]
    img_path = get_file(img_path)
    metadata = json.loads(dress_info["metadata"])
    return render_template(
        "dresspage.html",
        homepage_link=url_for("home"),
        dress_name=dress_info["name"],
        description=dress_info["description"],
        price=dress_info["price"],
        metadata=metadata,
        dress_image_link=url_for(".static", filename=img_path),
    )
