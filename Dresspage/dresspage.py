from flask import Blueprint,render_template,current_app 
from db_queries import getDress
dresspage_blueprint = Blueprint('dresspage', __name__, template_folder='templates', static_folder='static')

@dresspage_blueprint.route('/dresspage/<dressid>')
def dresspage(dressid):
    mysql = current_app.config['mysql']
    connection=mysql.connection
    dress_info=getDress(connection,dressid)
    print(dress_info)
    return render_template('Dresspage.html',
                            dress_image_link= 'https://www.nike.com/in/t/sportswear-t-shirt-dw59Bv')
      

