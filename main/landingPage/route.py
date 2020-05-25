"""
landing page/index/home page
"""
import mysql.connector as sql,logging,string
from main.dbConnect.db_conn import Connect

from flask import Blueprint,redirect, url_for, render_template
landing_page = Blueprint('landing_page', __name__)

@landing_page.route("/")
def index():
	testimony = get_testimonials()
	context = {'testimony':testimony}
	return render_template("landingPageHtml/landing-page.html", title="Home", **context)

# get testimonials from db
def get_testimonials():
	# instanciate database
	conn = Connect()
	# connect to the database
	con = conn.connect_db()
	# create cursor object
	myCur = con.cursor(buffered=True, dictionary=True)

	# basic user id query
	testimony_query = """
	select * from testimonials
	"""
	try:
		myCur.execute(testimony_query)
		# store results in an object
		data = myCur.fetchall()
		# close cursor
		myCur.close()
		# close connection
		con.close()
		# return the data
		return data
	except (sql.Error, sql.Warning) as e:
		print(e)
		# log the error
