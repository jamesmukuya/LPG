"""
landing page/index/home page
"""
from flask import Blueprint
from flask_login import current_user
from flask import redirect, url_for, render_template
landing_page = Blueprint('landing_page', __name__)

@landing_page.route("/")
def index():
	context = {}
	return render_template("landingPageHtml/landing-page.html", title="Home", **context)
