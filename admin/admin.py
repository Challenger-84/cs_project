from flask import Blueprint, render_template, url_for, request, flash, redirect

admin_blueprint = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@admin_blueprint.route('/admin')
def admin():
    return render_template('admin.html',
                            homepage_link = url_for('home') ,
                            profile_link = url_for('profile'),
                            addnewdress_link = url_for('admin.addnewdress'))

@admin_blueprint.route('/admin/addnewdress', methods=['GET', 'POST'])
def addnewdress():

    if request.method == 'POST':
        
        dress_name = request.form['dress_name']
        dress_description = request.form['description']
        dress_price = request.form['Price']

        flash("Dress added to the store database.")
        return redirect(url_for('admin.addnewdress'))
    else:
        return render_template('addnewdress.html')