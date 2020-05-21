from flask import (Blueprint, render_template)

coaching = Blueprint('coaching', __name__)

@coaching.route("/coaching")
def coaching_page():
  return render_template('coaching/coaching.html', title='Coaching')
