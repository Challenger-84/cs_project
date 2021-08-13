from flask import Blueprint,render_template
dresspage_blueprint = Blueprint('dresspage', __name__, template_folder='templates', static_folder='static')

@dresspage_blueprint.route('/dresspage/<dressid>')
def dresspage(dressid):
    return render_template('Dresspage.html',
                            dress_image_link= 'https://www.nike.com/in/t/sportswear-t-shirt-dw59Bv')
      
