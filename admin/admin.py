from flask import Blueprint, render_template, url_for

admin_blueprint = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@admin_blueprint.route('/admin')
def admin():
    return render_template('admin.html',
                            homepage_link = url_for('home') ,
                            profile_link = url_for('profile'),
                            addnewdress_link = url_for('admin.addnewdress'))

@admin_blueprint.route('/admin/addnewdress')
def addnewdress():
    return render_template('addnewdress.html')