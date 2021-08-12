from flask import Blueprint,render_template
dresspage_blueprint = Blueprint('dresspage', __name__, template_folder='templates', static_folder='static')

@dresspage_blueprint.route('/dresspage')
def dresspage():
    return render_template('Dresspage.html')
      

