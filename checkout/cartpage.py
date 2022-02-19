from flask import Blueprint, render_template, current_app, url_for

cartpage_blueprint = Blueprint('cartpage',__name__, template_folder='templates' ,static_folder='static')

@cartpage_blueprint.route('/cartpage')
def cartpage():
    # mysql connection
    mysql = current_app.config['mysql']
    connection=mysql.connection
    
    render_template('cartpage.html')