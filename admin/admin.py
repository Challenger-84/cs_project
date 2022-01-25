import os

from flask import Blueprint, render_template, url_for, request, flash, redirect, current_app, session
from utils.db_queries import add_dress, view_all_dress, view_all_users, deleteuser, update_user_account, del_dress
from utils.img_host import upload_file

admin_blueprint = Blueprint('admin', __name__, template_folder='templates', static_folder='static', url_prefix='/admin')


@admin_blueprint.route('/')
def admin():
    if session['user_type'] == 'admin':
        return render_template('admin.html',
                                homepage_link = url_for('root') ,
                                profile_link = url_for('profile'),
                                addnewdress_link = url_for('admin.addnewdress'))
    else:
        flash('You do not have permission to access this')
        return redirect(url_for('profile'))

@admin_blueprint.route('/addnewdress', methods=['GET', 'POST'])
def addnewdress():

    mysql = current_app.config['mysql']
    
    if request.method == 'POST':
        
        dress_name = request.form['dress_name']
        dress_description = request.form['description']
        dress_price = request.form['Price']
        dress_img = request.files['img_file']
        dress_stock = request.form['stock']

        # Uploading image file to dropbox
        dress_img.save(dress_img.filename)
        stored_path = upload_file(dress_img.filename)
        os.remove(dress_img.filename)

        conn = mysql.connection
        add_dress(conn,dress_name,dress_description,stored_path,dress_price, dress_stock)
        conn.close()
        
        flash("Dress added to the store database.")
        return redirect(url_for('admin.addnewdress'))
    else:
        return render_template('addnewdress.html',
                                add_dress_link = url_for('admin.addnewdress'),
                                view_dress_link = url_for('admin.viewalldress'),
                                view_user_link= url_for('admin.viewallusers'))

@admin_blueprint.route('/viewalldress')
def viewalldress():

    mysql = current_app.config['mysql']
    conn = mysql.connection
    dresses = view_all_dress(conn)
    conn.close
    return render_template('viewalldress.html', 
                            dresses = dresses,
                            add_dress_link = url_for('admin.addnewdress'),
                            view_dress_link = url_for('admin.viewalldress'),
                            view_user_link= url_for('admin.viewallusers'))

@admin_blueprint.route('/viewallusers')
def viewallusers():

    mysql = current_app.config['mysql']
    conn = mysql.connection

    users = view_all_users(conn)

    return render_template('viewallusers.html',
                            users = users, 
                            add_dress_link = url_for('admin.addnewdress'),
                            view_dress_link = url_for('admin.viewalldress'),
                            view_user_link= url_for('admin.viewallusers'), 
                            delete_dress_link = url_for('admin.deleteDress'))

@admin_blueprint.route('/deleteuser/<userid>/')
def deleteUser(userid):

    if session['user_type'] == 'admin':
        mysql = current_app.config['mysql']
        conn = mysql.connection

        deleteuser(conn, userid)
        conn.close()

        return redirect(url_for('admin.viewallusers'))
    
    else:
        flash('Not enough premission to access the page')
        redirect(url_for('root'))

@admin_blueprint.route('/changeuser/<userid>/<current_type>')
def changeUser(userid, current_type):

    if session['user_type'] == 'admin':
        mysql = current_app.config['mysql']
        conn = mysql.connection

        if current_type == 'user':
            update_user_account(conn, userid, 'admin')
        elif current_type == 'admin':
            update_user_account(conn, userid, 'user')

        return redirect(url_for('admin.viewallusers'))
    
    else:
        flash('Not enough premission to access the page')
        redirect(url_for('root'))

@admin_blueprint.route('/deletedress/<dressID>')
def deleteDress(dressID):

    if session['user_type'] == 'admin':
        mysql = current_app.config['mysql']
        conn = mysql.connection

        del_dress(conn, dressID)

        return redirect(url_for('admin.viewalldress'))

    else:
        flash('Not enough premission to do that action')
        redirect(url_for('root'))
