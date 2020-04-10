"""
flask initialization modules
blueprint import and registration
"""
from flask import Flask

app = Flask(__name__)

# change this
app.config['SECRET_KEY'] = '7daf12b8731868c589b15b625907dd7b'

from main.landingPage.route import landing_page

app.register_blueprint(landing_page)
