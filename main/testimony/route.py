"""
testimonial controller
"""
from main import app
import mysql.connector as sql,logging,string
#from main.model.user import User
from main.dbConnect.db_conn import Connect
from flask import (Blueprint, render_template, session,
                 flash, redirect, request, url_for)

testimony = Blueprint('testimony', __name__)

@testimony.route("/testimony/new", methods=["GET", "POST"])
def add_testimony():
  # only employees have access to the page
  if session.get('is_staff'):
    if request.method == "POST":
      # add a testimony and redirect to main page
      client_name = request.form['client_name'].strip()
      client_name = string.capwords(client_name)
      client_job = request.form['client_job'].strip()
      client_job = string.capwords(client_job)
      testimony = request.form['testimony'].strip()
      # insert into db
      insert_testimony(client_name, client_job, testimony)
      return redirect(url_for('landing_page.index'))
    return render_template('testimony/testimony.html',title='New Testimony')
  return redirect(url_for('user_auth.staff_login'))

def insert_testimony(client_name,client_job,testimony):
    """
    insert testimony data into database
    """
    # instanciate database
    conn = Connect()
    # connect to the database
    con = conn.connect_db()
    # create cursor object
    myCur = con.cursor(buffered=True, dictionary=True)

    # basic user id query
    testimony_query = """
    insert into testimonials (client_name,client_job,testimony)
    values (%(client_name)s,%(client_job)s,%(testimony)s)
    """
    try:
        # user session insert
        data = {'client_name': client_name,'client_job':client_job,
                     'testimony': testimony}
        myCur.execute(testimony_query, data)

        # commit the data
        con.commit()

        # close cursor
        myCur.close()

        # close connection
        con.close()
        flash(f'testimony for {client_name} created', 'success')
    except (sql.Error, sql.Warning) as e:
        # log the error
        logging.basicConfig(filename=app.config['LOGGING_FOLDER'] + 'user_testimony.log',
                            level=logging.WARN)
        logging.warning(f'{e}')
        flash('could not create user testimony', 'error')
