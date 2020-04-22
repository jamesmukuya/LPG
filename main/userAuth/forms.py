from flask_wtf import FlaskForm
from wtforms.validators import (DataRequired, Length, Email,EqualTo)
from wtforms import StringField, PasswordField, SubmitField

class RegisterForm(FlaskForm):
    """
    create a form instance for a csrf protection
    """
    firstName = StringField(label='first name', validators=[DataRequired(),
                Length(min=2, max=15, message="Min length is 2 and max is 15")])
    lastName = StringField(label='last name', validators=[DataRequired(),
                Length(min=2, max=15, message="Min length is 2 and max is 15")])
    password = PasswordField(label='password', validators=[DataRequired(),
                Length(min=4, message="Min length is 4")])
    confirmPassword = PasswordField(label='password', validators=[DataRequired(),
                EqualTo('password')])
    #email = StringField(label='email', validators=[Email(
        #message="please enter a valid email address")])
    submit=SubmitField(label='Register')

class LoginForm(FlaskForm):
    """
    flask login form
    """
    password = PasswordField(label='password', validators=[DataRequired(),
                Length(min=4, message="Min length is 4")])
    email = StringField(label='email', validators=[Email(
        message="please enter a valid email address")])
    submit = SubmitField(label='Login')
