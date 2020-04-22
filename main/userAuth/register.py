"""
register new user
"""
from flask_bcrypt import Bcrypt
from main.userAuth.forms import RegisterForm
from flask import (Blueprint, render_template,
                   flash, redirect, request, url_for)

sign_up = Blueprint('sign_up', __name__)

@sign_up.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    bcrypt = Bcrypt()
    context = {'form': form}
    if request.method == 'POST':
        # get email and check if exists in database
        email = request.form['user_email']
        #print(first_name, last_name, email, user_name)
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            #first_name = request.form['first_name']
            #last_name = request.form['last_name']
            first_name = form.firstName.data
            last_name=form.lastName.data
            user_name = first_name + '.' + last_name
            print('validated', email, hashed_password)
            flash(f'Account created for {user_name}', 'success')
            return redirect(url_for('landing_page.index'))
        else:
            print('an error occured during validation')
    return render_template('user_auth/register.html', title='Register', **context)
