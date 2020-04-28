"""
login and registered user
"""
from datetime import datetime
import mysql.connector as sql
from flask_login import login_user
from main.userAuth.user import User
from main import login_manager,bcrypt
from main.dbConnect.db_conn import Connect
from main.userAuth.forms import LoginForm, RegisterForm
from flask import (Blueprint, render_template,
                   flash, redirect, request, url_for)

user_auth = Blueprint('user_auth', __name__)

@user_auth.route("/login", methods=["GET", "POST"])
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
            first_name = user_mail.get('first_name').capitalize()
            last_name = user_mail.get('last_name').capitalize()
            user_password=user_mail.get('user_password')
            if user_mail and bcrypt.check_password_hash(user_password,password):
                login_user(user)
                flash(f'Welcome {last_name}, {first_name}','login success')
                return redirect(url_for('landing_page.index'))
            #connection(email)
            flash(f'Your email or password is incorrect', 'error')
        else:
            # user is not registered. email or password is not correct
            flash(f'unknown error has occured, please contact admin\
                    for assistance', 'error')
    return render_template('user_auth/login.html', title='Login', **context)


@user_auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    #bcrypt = Bcrypt()
    context = {'form': form}
    if request.method == 'POST':
        if form.validate_on_submit():
            # get email and check if exists in database
            email = request.form['user_email']
            user = User()
            user_mail = user.get_user(email)
            try:
                if user_mail.get('email') == email:
                    print('email already exists')
                    flash(f'email address already exists. login?','error')
                    return render_template('user_auth/register.html', title='Register', **context)
                #print('user mail data',user_mail.get('email'))
            
            # the user does not exist
            except AttributeError:
                #pass
                hashed_password = bcrypt.generate_password_hash(
                    form.password.data).decode('utf-8')
                first_name = form.firstName.data.capitalize()
                last_name = form.lastName.data.capitalize()
                # insert into basic user details db
                register_user(first_name=first_name, last_name=last_name, email=email,
                user_password=hashed_password)
                
                # login registered user
                #user=User(name=first_name,email=email)
                #login_user(user)

                flash(f'Account created for {last_name}, {first_name}', 'success')
                return redirect(url_for('landing_page.index'))
            # continue registering
        else:
            print('some error occured')
            flash('an error occured during validation','error')
    return render_template('user_auth/register.html', title='Register', **context)

def register_user(first_name, last_name, email, user_password):
    # instanciate database
    conn = Connect()
    # connect to the database
    con = conn.connect_db()
    # create cursor object
    myCur = con.cursor()

    # basic data query
    insert_basic_query = (
        "INSERT INTO basic_user_details (first_name, last_name, email, user_password) "
        "VALUES (%s, %s, %s, %s)"
    )
    basic_data = first_name, last_name, email, user_password

    # user history query
    insert_basic_history_query = (
        "insert into user_details_history"
        "(basic_user_details_id)"
        "value(%(basic_user_details_id)s)"
    )

    # user registration query
    insert_user_reg_query = (
        "insert into user_registration"
        "(date_registered,basic_user_details_id)"
        "values(%(date_registered)s,%(basic_user_details_id)s)"
    )
    try:
        # execute the query
        myCur.execute(insert_basic_query, basic_data)

        # basic detail history insert. get id from previous insert
        usr_id = myCur.lastrowid
        myCur.execute(insert_basic_history_query, {
                      'basic_user_details_id': usr_id})

        # registration data insert. get id from previous insert
        reg_data = {
            'date_registered': datetime.utcnow(),
            'basic_user_details_id': usr_id
            }
        myCur.execute(insert_user_reg_query, reg_data)
        # commit the data
        con.commit()

        # close cursor
        myCur.close()

        # close connection
        con.close()
    except (sql.Error, sql.Warning) as error:
        flash('could not create user','error')

# monitor this function
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
    return redirect(url_for('user_auth.login'))

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
