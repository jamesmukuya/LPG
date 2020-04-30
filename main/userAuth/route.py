"""
login and registered user
"""
from datetime import datetime
import mysql.connector as sql
#from flask_login import login_user,logout_user,current_user
#from main.userAuth.user import User
from main.model.user import User
from main import bcrypt  # login_manager,
from main.dbConnect.db_conn import Connect
from main.userAuth.forms import LoginForm, RegisterForm
from flask import (Blueprint, render_template, session,
                   flash, redirect, request, url_for)

user_auth = Blueprint('user_auth', __name__)

session_in_data = {'logged_in':True}
#session_out_data = {'logged_in':None}

@user_auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    context = {'form': form}
    if request.method == "POST":
        if form.validate_on_submit():
            password = form.password.data
            email = form.email.data
            #print(email)
            # check if user data exists in database
            user = User()
            user_data = user.get_user(email)
            first_name = user_data.get('first_name').capitalize()
            last_name = user_data.get('last_name').capitalize()
            user_password = user_data.get('user_password')
            if user_data and bcrypt.check_password_hash(user_password, password):
                # start a session with the user
                session_in_data.update(user_data)
                session.update(session_in_data)
                flash(f'{last_name}, {first_name}', 'Welcome')
                # insert session data in database


                # get the current page of the user


                # redirect the user to the required page
                return redirect(url_for('landing_page.index'))
            
            # the email or password is incorrect
            flash(f'Your email or password is incorrect', 'error')
        else:
            # another error occured
            flash(f'unknown error has occured, please contact admin\
                    for assistance', 'error')
    return render_template('user_auth/login.html', title='Login', **context)


@user_auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
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
            
            # the user does not exist
            except AttributeError:
                # generate a secret password
                hashed_password = bcrypt.generate_password_hash(
                    form.password.data).decode('utf-8')
                first_name = form.firstName.data.capitalize()
                last_name = form.lastName.data.capitalize()
                # insert into basic user details db
                register_user(first_name=first_name, last_name=last_name, email=email,
                user_password=hashed_password)
                
                # login registered user and start a session
                session['logged_in'] = True
                session['first_name'] = first_name
                session['last_name'] = last_name

                # commit session to database


                flash(f'Account created for {last_name}, {first_name}', 'success')
                return redirect(url_for('landing_page.index'))
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
    except (sql.Error, sql.Warning):
        flash('could not create user','error')

@user_auth.route("/logout")
def logout():
    [session.pop(key) for key in list(session.keys())]
    return redirect(url_for('user_auth.login'))

