"""
are we a fit page
"""
from flask import Blueprint
from flask import redirect, url_for, render_template
areWeAfit_page = Blueprint('areWeAfit_page', __name__)

@areWeAfit_page.route("/are-we-a-fit")
def index():
	context = {}
	return render_template("areWeAfitHtml/are-we-a-fit.html", title="Are we a fit", **context)
