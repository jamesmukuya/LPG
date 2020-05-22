from flask import (Blueprint, render_template)

services = Blueprint('services', __name__)

@services.route("/services")
def services_page():
  return render_template('services/services.html', title='Services')

@services.route("/how-it-all-works")
def how_it_works_page():
  return render_template('services/how-it-all-works.html', title="How it Works")
  
@services.route("/corporate-community")
def corporate_community_page():
  return render_template('services/corporate-community.html', title="Corporate & Community")
