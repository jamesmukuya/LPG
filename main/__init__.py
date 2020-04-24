"""
flask initialization modules
blueprint import and registration
"""
from flask import Flask
from config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)

from main.landingPage.route import landing_page
from main.areWeAfit.route import areWeAfit_page
from main.fileUpDownloads.route import download_file, upload_file, download_route
from main.userAuth.login import sign_in
from main.userAuth.register import sign_up
from main.resources.route import resources

app.register_blueprint(landing_page)
app.register_blueprint(areWeAfit_page)
app.register_blueprint(download_file)
app.register_blueprint(upload_file)
app.register_blueprint(download_route)
app.register_blueprint(sign_in)
app.register_blueprint(sign_up)
app.register_blueprint(resources)
