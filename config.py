"""
environment configuration files
"""
import os

class BaseConfig:
    """
    Base configuration attributes
    """
    DEBUG = False
    TESTING = False
    SECRET_KEY = '7daf12b8731868c589b15b625907dd7b'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    # SOME OTHER CONFIG VARS e.g DB credentials


class DevConfig(BaseConfig):
    """
    Development configuration attributes
    """
    DEBUG = True
    TESTING = True
    MISC_UPLOAD_FOLDER = os.getcwd()+r"/main/static/documents/admin/misc/"
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
    pass
