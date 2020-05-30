"""
login and registered user
"""
#from flask_login import login_user,logout_user,current_user

import logging
import smtplib
import os
import glob
import json
from email.message import EmailMessage
from main import bcrypt, app
from datetime import datetime
import mysql.connector as sql
from main.model.user import User
from main.model.UserReset import UserTable
from main.dbConnect.db_conn import Connect
from main.userAuth.forms import LoginForm, RegisterForm, ResetPasswordForm
from flask import (Blueprint, render_template, session,
                   flash, redirect, request, url_for)

user_auth = Blueprint('user_auth', __name__)

# session data
session_in_data = {'logged_in': True}
session_staff_data = {'logged_in': True, 'is_staff': True}


@user_auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    context = {'form': form}
    if request.method == "POST":
        #if form.validate_on_submit():
        password = form.password.data
        email = form.email.data
        # check if user data exists in database
        user = User()
        user_data = user.get_user(email)
        first_name = user_data.get('first_name').capitalize()
        last_name = user_data.get('last_name').capitalize()
        user_password = user_data.get('user_password')

        if user_data and bcrypt.check_password_hash(user_password, password):
            #print('password from db:',user_password)
            # start a session with the user
            session_in_data.update(user_data)
            session.update(session_in_data)
            flash(f'{last_name}, {first_name}', 'Welcome')
            # print(session)
            # insert session data in database
            user_session_in(user_data.get('id'))

            # get the current page of the user

            # redirect the user to the required page
            return redirect(url_for('landing_page.index'))

        # the email or password is incorrect
        flash(f'Your email or password is incorrect', 'error')
        # log the error
        logging.basicConfig(filename=app.config['LOGGING_FOLDER'] + 'user_auth.log',
                            level=logging.WARN)
        logging.warning('incorrect username/password')

        #else:
        #    # another error occured
        #    flash(f'unknown error has occured, please contact admin\
        #            for assistance ', 'error')
        #    # log the error
        #    logging.basicConfig(filename=app.config['LOGGING_FOLDER'] + 'user_auth.log',
        #                        level=logging.ERROR)
        #    logging.error('error occured')
    return render_template('user_auth/login.html', title='Login', **context)


@user_auth.route("/staff-login", methods=["GET", "POST"])
def staff_login():
    # create an instance of the form
    form = LoginForm()
    # pass the form objects to context
    context = {'form': form}

    # get the post credentials
    if request.method == "POST":
        staff_number = request.form['staff_number']
        password = form.password.data

        # create an instance of User
        staff = User()
        # pass in the staff number for query
        staff_data = staff.get_staff(staff_number)
        staff_id = staff.get_staff_id(staff_number)
        staff_password = staff_data.get('user_password')
        # check if credentials provided are correct
        if staff_data and bcrypt.check_password_hash(staff_password, password):
            # start a session with the user
            session['staff_id'] = staff_id.get('id')
            session_staff_data.update(staff_data)
            # update the entire session
            session.update(session_staff_data)

            last_name = staff_data.get('last_name')
            first_name = staff_data.get('first_name')

            flash(f'{last_name}, {first_name}', 'Welcome')
            # insert session data in database

            # get the current page of the user

            # redirect the user to the required page ###
            return redirect(url_for('landing_page.index'))

        # the email or password is incorrect
        flash(f'Your staff number or password is incorrect', 'error')
        # log the error
        logging.basicConfig(filename=app.config['LOGGING_FOLDER'] + 'user_auth.log',
                            level=logging.WARN)
        logging.warning('incorrect username/password')
        return render_template('user_auth/staff.html', title='Staff Login', **context)

    return render_template('user_auth/staff.html', title='Staff Login', **context)


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
                    flash(f'email address already exists. login?', 'error')
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

                flash(
                    f'Account created for {last_name}, {first_name}', 'success')

                # commit session to database
                # created in the register method.
                # TODO...A new user does not submit a logout session
                # for some reason

                return redirect(url_for('landing_page.index'))
        else:
            #print('some error occured')
            flash('an error occured during validation', 'error')
            # log the error
            logging.basicConfig(filename=app.config['LOGGING_FOLDER'] + 'user_reg.log',
                                level=logging.WARN)
            logging.warning('Validation Error')
    return render_template('user_auth/register.html', title='Register', **context)


def send_reset_email(user):
    """
    send reset email to user email provided
    """
    u = UserTable()
    token = u.get_reset_token()
    # get data from fields change to noreply@livingpeak.org
    sending_addr = 'info@techpoint.systems'
    msg = EmailMessage()
    msg['subject'] = 'Password Reset'
    msg['From'] = f'noreply <{sending_addr}>'
    msg['To'] = user

    msg.set_content(f"""To reset your password, visit the following link:
{url_for('user_auth.password_reset',token=token,_external=True)}

If you did not send this request, please ignore and no changes will be made
""")

    # get credentials from file
    credentials = get_auth()
    with smtplib.SMTP_SSL(credentials[0], 465) as smtp:
        smtp.login(credentials[1], credentials[2])
        smtp.send_message(msg)

# get the credentials from secure file


def get_auth():
    for files in glob.iglob('**/*.json', recursive=True):
        with open(files) as f:
            data = json.load(f)
            url = data.get('test_SSL_URL')
            user_name = data.get('test_email_user')
            user_pass = data.get('test_email_pass')
    return url, user_name, user_pass

@user_auth.route('/password-link', methods=['GET', 'POST'])
def password_reset_request():
    form = ResetPasswordForm()
    context = {'form': form}

    # user cannot forget password while logged in
    if session.get('logged_in'):
        return redirect(url_for('landing_page.index'))
    if request.method == 'POST':
        # get user data and confirm they exist in database
        email = request.form['email']
        user = UserTable()
        user_mail = user.verify_email(email)

        if user_mail != None:
            send_reset_email(email)
            flash('password reset link has been sent to your email. If you do not\
			receive within 10 minutes please contact us for assistance', 'success')
            return redirect(url_for('user_auth.login'))

        flash(
            f'The email does not exist.{url_for("user_auth.register")} Register?', 'error')
    return render_template('user_auth/password-link.html', **context)

# route to display form with password entry to change password
@user_auth.route('/password-reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    form = ResetPasswordForm()
    context = {'form': form}
    # if user is currently logged in and tries to reset password
    # redirect to home page
    if session.get('logged_in'):
        return redirect(url_for('landing_page.index'))

    user = UserTable()
    user = user.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'error')
        return redirect(url_for('user_auth.password_reset_request'))

    #print('the token is still okay',user)
    # check request type
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')

        # both passwords match, update record in db
        update_password(user_id=user.id, new_password=hashed_password)
        return redirect(url_for('user_auth.login'))
    # return login form
    flash('Your passwords do not match','error')
    return render_template('user_auth/password-reset.html',
                           title='Password Reset', **context)


def update_password(user_id, new_password):
    """
    query takes in user id and new hashed password
    """
    conn = Connect()
    con = conn.connect_db()
    myCur = con.cursor()
    
    update_pass_query = """
    update basic_user_details set user_password = %(user_password)s
    where basic_user_details.id = %(id)s
    """
    update_data = {
        'id': user_id,
        'user_password': new_password
    }
    try:
        myCur.execute(update_pass_query, update_data)
        con.commit()
        myCur.close()
        con.close()
        flash('Your password has been changed', 'success')
    except(sql.Error, sql.Warning) as e:
        print(e)
        flash('could not update your password, kindly contact us for\
             assistance', 'error')


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

    # user session
    usr_sess_query = """
                insert into user_session (login_time,user_registration_id)
                values(%s,%s)
                """
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
        reg_id = myCur.lastrowid

        # user session insert
        sess_data = datetime.utcnow(), reg_id
        myCur.execute(usr_sess_query, sess_data)
        session['user_session_id'] = reg_id

        # commit the data
        con.commit()

        # close cursor
        myCur.close()

        # close connection
        con.close()
    except (sql.Error, sql.Warning) as e:
        # log the error
        logging.basicConfig(filename=app.config['LOGGING_FOLDER'] + 'user_reg.log',
                            level=logging.ERROR)
        logging.warning(f'{e}')
        flash('could not create user', 'error')


def user_session_in(uid):
    """
    uid=basic user registration id.
    insert user session data into database
    """
    # instanciate database
    conn = Connect()
    # connect to the database
    con = conn.connect_db()
    # create cursor object
    myCur = con.cursor(buffered=True, dictionary=True)

    # basic user id query
    usr_id_query = """
    select user_registration.id from user_registration where 
    basic_user_details_id = %(basic_user_details_id)s
    """

    # user session query
    usr_sess_query = """
                insert into user_session (login_time,user_registration_id)
                values(%(login_time)s,%(user_registration_id)s)
                """
    try:
        # get user registration id
        myCur.execute(usr_id_query, {'basic_user_details_id': uid})
        reg_id = myCur.fetchone()
        reg_id = reg_id['id']

        # user session insert
        sess_data = {'login_time': datetime.utcnow(),
                     'user_registration_id': reg_id}
        myCur.execute(usr_sess_query, sess_data)

        # get the sesssion id and pass to session object
        sess_id = myCur.lastrowid
        session['user_session_id'] = sess_id

        # commit the data
        con.commit()

        # close cursor
        myCur.close()

        # close connection
        con.close()
    except (sql.Error, sql.Warning) as e:
        # log the error
        logging.basicConfig(filename=app.config['LOGGING_FOLDER'] + 'user_session.log',
                            level=logging.WARN)
        logging.warning(f'{e}')
        flash('could not create user session', 'error')


def user_session_out(sid):
    """
    sid = user session id from session object.
    update user session logout time and total sessio time
    """
    # instanciate database
    conn = Connect()
    # connect to the database
    con = conn.connect_db()
    # create cursor object
    myCur = con.cursor(buffered=True, dictionary=True)

    # user session time update
    usr_sess_query = """
    update user_session set logout_time = %(logout_time)s
    where id = %(id)s
    """

    # user session total time
    usr_time_query = """
    update user_session set session_time = logout_time-login_time
    where id = %(id)s
    """

    try:
        # user session update
        sess_data = {'logout_time': datetime.utcnow(),
                     'id': sid}
        myCur.execute(usr_sess_query, sess_data)

        myCur.execute(usr_time_query, {'id': sid})

        # commit the data
        con.commit()

        # close cursor
        myCur.close()

        # close connection
        con.close()
    except (sql.Error, sql.Warning) as e:
        # log the error
        logging.basicConfig(filename=app.config['LOGGING_FOLDER'] + 'user_auth.log',
                            level=logging.WARN)
        logging.warning(f'{e}')
        flash('could not update user session', 'error')


@user_auth.route("/logout")
def logout():
    # record logout time in database
    user_session_out(session.get('user_session_id'))
    # if session was user redirect to user login else staff login
    if session.get('is_staff') == True:
        # remove session cookies
        [session.pop(key) for key in list(session.keys())]
        return redirect(url_for('user_auth.staff_login'))

    # remove session cookies
    [session.pop(key) for key in list(session.keys())]
    return redirect(url_for('user_auth.login'))
