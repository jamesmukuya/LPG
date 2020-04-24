from flask_wtf import FlaskForm
from wtforms.validators import (DataRequired, Email)
from wtforms import StringField

class ResourceRequestForm(FlaskForm):
    """
    flask resource request form
    """
    email = StringField(label='email', validators=[DataRequired(),Email(
        message="please enter a valid email address")])
    #submit = SubmitField(label='Login')
