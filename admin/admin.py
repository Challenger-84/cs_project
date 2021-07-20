from flask import Blueprint, render_template, url_for, request, flash, redirect, current_app
from db_queries import add_dress, view_all_dress, view_all_users

admin_blueprint = Blueprint('admin', __name__, template_folder='templates', static_folder='static', url_prefix='/admin')


@admin_blueprint.route('/')
def admin():
    return render_template('admin.html',
                            homepage_link = url_for('home') ,
                            profile_link = url_for('profile'),
                            addnewdress_link = url_for('admin.viewallusers'))

@admin_blueprint.route('/addnewdress', methods=['GET', 'POST'])
def addnewdress():

    mysql = current_app.config['mysql']
    
    if request.method == 'POST':
        
        dress_name = request.form['dress_name']
        dress_description = request.form['description']
        dress_price = request.form['Price']
        dress_imgurl = request.form['img_url']
        dress_stock = request.form['stock']

        conn = mysql.connection

        add_dress(conn, dress_name,dress_description, dress_imgurl, dress_price, dress_stock)
        conn.close()
        
        flash("Dress added to the store database.")
        return redirect(url_for('admin.addnewdress'))
    else:
        return render_template('addnewdress.html')

@admin_blueprint.route('/viewalldress')
def viewalldress():

    mysql = current_app.config['mysql']
    conn = mysql.connection
    dresses = view_all_dress(conn)
    print(dresses)
    conn.close
    return render_template('viewalldress.html', 
                            dresses = dresses)

@admin_blueprint.route('/viewallusers')
def viewallusers():

    mysql = current_app.config['mysql']
    conn = mysql.connection

    users = view_all_users(conn)

    return render_template('viewallusers.html',
                            users = users)