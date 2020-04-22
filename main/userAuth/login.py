"""
login registered user
"""
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
            password = form.password.data
            email = form.email.data
            print('validated', password, email)
            flash(f'login success {email}', 'success')
            return redirect(url_for('landing_page.index'))
        else:
            print('not validated')
    return render_template('user_auth/login.html', title='Login', **context)
