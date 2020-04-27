"""
login registered user
"""
from main import login_manager
from flask_login import login_user
from main.userAuth.user import User
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
        if form.validate_on_submit():
            password = form.password.data
            email = form.email.data
            #print(email)
            # check if user exists in database
            user = User()
            user_mail = user.get_user(email)
            first_name = user_mail.get('first_name')
            last_name = user_mail.get('last_name')
            if user_mail and password == 'acomplexpass':
                login_user(user)
                flash(f'Welcome {last_name}, {first_name}','login success')
                return redirect(url_for('landing_page.index'))
            #connection(email)
            #print('invalid credentials')
            flash(f'Your email or password is incorrect', 'error')
            #return redirect(url_for('landing_page.index'))
        else:
            # user is not registered. email or password is not correct
            flash(f'unknown error has occured, please contact admin\
                    for assistance', 'error')
            #print('not validated')
    return render_template('user_auth/login.html', title='Login', **context)


@login_manager.user_loader
def load_user(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    if user_id is not None:
        user = User()
        user_mail = user.get_id()
        #print('user_id',user_id)
        return user_mail
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.','error')
    return redirect(url_for('sign_in.login'))

"""
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
"""
