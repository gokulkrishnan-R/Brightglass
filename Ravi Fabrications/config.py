#All configurations setups are here:

# config.py
import os
from flask_session import Session
from flask import Flask
from flask_mail import Mail
from datetime import timedelta
#import app
#from.routes import *

"""random=os.urandom(24)
hex_boi=hex(random)
print("the hex num is",hex_boi)
"""
class Config:
    BASE_DIR=os.path.abspath(os.path.dirname(__file__))
    TEMPLATE_DIR=os.path.join(BASE_DIR,"templates")
    STATIC_DIR = os.path.join(BASE_DIR, "static")           # Path to the static folder
    IMAGE_DIR=os.path.join(BASE_DIR, "images") #This is for the path of images folder
    SECRET_KEY = '95af72b414ec8701dc2885e73170d333fbe020575738dbdc'  # Secure key for sessions and CSRF protection
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:/Users/g/Downloads/Ravi Fabrications/instance/site.db'  # URI for SQLite database
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable overhead of tracking modifications
    DEBUG = False  # Disable debug mode (can enable in development config)
    WTF_CSRF_ENABLED = True
    #Adding all necessary e-Mail Configurations
    MAIL_SERVER="smtp.gmail.com"
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USE_SSL=False
    MAIL_USERNAME="scarywolf98@gmail.com"
    MAIL_PASSWORD="april281998"
    MAIL_DEFAULT_SENDER="gokulkrish981997@gmail.com"
    #Adding all necessary Session configirations
    SESSION_TYPE = 'filesystem'  # Store session data on the filesystem
    SESSION_PERMANENT = False  # Session will not be permanent
    SESSION_USE_SIGNER = True  # Use a signer for the session cookie
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to the cookie
    SESSION_COOKIE_SECURE = False  # Set to True if using HTTPS
    PERMANENT_SESSION_LIFETIME = timedelta(days=365)  # Session lifetime
    #WE can even set timedelta(days=25)  #WE can even set the session upto different timings.

    
    """# Flask-Mail Configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use your mail server
    app.config['MAIL_PORT'] = 587  # For starttls
    app.config['MAIL_USE_TLS'] = True  # Enable TLS
    app.config['MAIL_USE_SSL'] = False  # Disable SSL
    app.config['MAIL_USERNAME'] = 'scarywolf98@gmail.com'  # Your email address
    app.config['MAIL_PASSWORD'] = 'april281998'  # Your email password
    app.config['MAIL_DEFAULT_SENDER'] = 'gokulkrish981997@gmail.com'  # Default sender
    """

class DevelopmentConfig(Config):
    DEBUG = True  # Enable debug mode for development
    #SQLALCHEMY_DATABASE_URI = 'sqli
    
"""
class ProductionConfig(Config):
    DEBUG = False  # Production should not use debug mode
    SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/prod_db'  # Example production DB URI
"""