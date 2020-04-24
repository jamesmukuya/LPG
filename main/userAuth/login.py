"""
login registered user
"""

from main.dbConnect.db_conn import Connect
from main.userAuth.forms import LoginForm
from flask import (Blueprint, render_template,
                   flash, redirect, request, url_for)

sign_in = Blueprint('sign_in', __name__)

@sign_in.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    context = {'form': form}
    if request.method == "POST":
        #email = request.form['email']
        if form.validate_on_submit():
            #password = form.password.data
            email = form.email.data
            # check if user exists in database
            connection(email)
            #flash(f'login success {email}', 'success')
            #return redirect(url_for('landing_page.index'))
        else:
            # user is not registered. email or password is not correct
            #flash(f'your email or password is not correct', 'error')
            print('not validated')
    return render_template('user_auth/login.html', title='Login', **context)

# we pass in the email since it is the unique variable
def connection(e):
    # create a new object from class
    conn = Connect()
    # establish the connection
    con = conn.connect_db()
    # create a cursor
    myCur = con.cursor()
    # make a query on the basic_user_details table
    query="select * from basic_user_details where email = %(email)s"
    print(query)
    # execute the query
    myCur.execute(query, {'email':e})    
    # get data from the returned query object
    data = myCur.fetchone()
    # return required data
    print(data)
    return data

