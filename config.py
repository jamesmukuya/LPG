"""
environment configuration files
"""
import os,glob, json

class BaseConfig:
    """
    Base configuration attributes
    """
    DEBUG = False
    TESTING = False
    SECRET_KEY = '7daf12b8731868c589b15b625907dd7b'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'xlsx', 'xls', 'pub', 'csv', 'ppt', 'pptx'}
    ALLOWED_THUMBNAILS = {'png', 'jpg', 'jpeg'}
    UPLOAD_FOLDER = os.getcwd()+r"/main/static/documents/"
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024
    # SOME OTHER CONFIG VARS e.g DB credentials

class DevConfig(BaseConfig):
    """
    Development configuration attributes
    """
    DEBUG = True
    TESTING = True
    MISC_UPLOAD_FOLDER = os.getcwd()+r"/main/static/documents/client/misc/"
    LOGGING_FOLDER = os.getcwd()+r"/main/appLogger/"
    # SOME OTHER CONFIG VARS

class TestConfig(BaseConfig):
    """
    Testing configuration attributes
    """
    TESTING = True

class ProductionConfig(BaseConfig):
    """
    Production configuration attributes. Should be highly secretive.
    Recommended to obtain from environment variables or a private server.
    """
    for files in glob.iglob('**/*.json', recursive=True):
        with open(files) as f:
            data = json.load(f)
            url = data.get('prod_SSL_URL')
            user_name = data.get('prod_email_user')
            user_pass = data.get('prod_email_pass')

    LOGGING_FOLDER = os.getcwd() + r"/main/appLogger"
    MAIL_SERVER = url
    MAIL_PORT = 465
    # place all options here e.g noreply name and its pass
    MAIL_USERNAME = user_name
    MAIL_PASSWORD = user_pass
