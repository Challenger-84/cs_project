from flask import Blueprint, render_template, current_app, url_for

from utils.db_queries import getDress
from utils.img_host import get_file

dresspage_blueprint = Blueprint(
    "dresspage", __name__, template_folder="templates", static_folder="static"
)


@dresspage_blueprint.route("/dresspage/<dressid>")
def dresspage(dressid):
    mysql = current_app.config["mysql"]
    connection = mysql.connection
    dress_info = getDress(connection, dressid)

    img_path = dress_info[3]
    img_path = get_file(img_path)

    return render_template(
        "dresspage.html",
        homepage_link=url_for("home"),
        dress_name=dress_info[1],
        description=dress_info[2],
        dress_image_link=url_for(".static", filename=img_path),
    )
