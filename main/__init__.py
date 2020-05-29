"""
flask initialization modules
blueprint import and registration
"""
from flask import Flask
from config import DevConfig
from flask_bcrypt import Bcrypt

# app instances
app = Flask(__name__)
app.config.from_object(DevConfig)

# login management
#login_manager = LoginManager()
#login_manager.login_view = 'users.login'
#login_manager.login_message_category = 'info'
#login_manager.init_app(app)

# password hashing
bcrypt = Bcrypt()
bcrypt.init_app(app)

# blueprint routes
from main.landingPage.route import landing_page
from main.areWeAfit.route import areWeAfit_page
from main.fileUpDownloads.route import download_file, upload_file
from main.userAuth.route import user_auth
from main.services.route import services
from main.resources.route import resources
from main.contact.route import contact
from main.testimony.route import testimony
from main.blog.route import blog

# blueprint routes registration
app.register_blueprint(landing_page)
app.register_blueprint(areWeAfit_page)
app.register_blueprint(download_file)
app.register_blueprint(upload_file)
app.register_blueprint(user_auth)
app.register_blueprint(services)
app.register_blueprint(resources)
app.register_blueprint(contact)
app.register_blueprint(testimony)
app.register_blueprint(blog)
