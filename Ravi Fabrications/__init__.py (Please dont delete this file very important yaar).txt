from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from .models import db, User, Order
from flask_wtf import CSRFProtect
from sqlalchemy import text
from flask_mail import Mail,Message
from flask_session import Session

migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()
session = Session()


# Routes for user login and other works
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__, template_folder=Config.TEMPLATE_DIR, static_folder=Config.STATIC_DIR)
    app.config.from_object(Config)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/g/Downloads/Ravi Fabrications/instance/site.db'
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    # Initialize Flask-Mail Configuration
    mail.init_app(app)
    #Initializing the Session Here.
    session.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.unauthorized_view = 'auth.unauthorized'

    with app.app_context():
        #db.drop_all()
        db.create_all()
        #db.session.commit()
        #db.session.execute(text(""" DROP TABLE IF EXISTS ('customer_booking', 'customer_bookings', 'customer_quotes', 'orders', 'quotes', 'users'),('?','?','?','?','?','?') """))
        #db.session.execute(text("""
            #DROP TABLE IF EXISTS customer_booking, customer_bookings, customer_quotes, orders, quotes, users;
        #"""))  
        
        '''from sqlalchemy import text

        # This will drop each table in one go but needs separate execution
        statements = [
            "DROP TABLE IF EXISTS customer_booking;",
            "DROP TABLE IF EXISTS customer_bookings;",
            "DROP TABLE IF EXISTS customer_quotes;",
            "DROP TABLE IF EXISTS orders;",
            "DROP TABLE IF EXISTS quotes;",
            "DROP TABLE IF EXISTS users;"
        ]

        for statement in statements:
            db.session.execute(text(statement))
            db.session.commit()'''

    from .routes import main, auth, admin, user_panel, user_signup, about_panel, profile_update_panel, delete_orders, book_slot,forget_password,reset_password,submit_quotation,site_owner,download_file,delete_profile,owner_profile_deletion,order_status
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    app.register_blueprint(user_panel)
    app.register_blueprint(user_signup)
    app.register_blueprint(about_panel)
    app.register_blueprint(profile_update_panel)
    app.register_blueprint(delete_orders)  # Ensure this is registered
    app.register_blueprint(book_slot)
    app.register_blueprint(forget_password) #Reset passoword Blueprint\
    app.register_blueprint(reset_password) #For resetting 
    app.register_blueprint(submit_quotation) #For Quotation
    app.register_blueprint(site_owner) #Specially Access to the Site-Owner
    app.register_blueprint(download_file) #For Downloading Purpose  
    #app.register_blueprint(generate_random) #For random generation of Order ID's
    app.register_blueprint(delete_profile) #For deleting the user profile. 
    app.register_blueprint(owner_profile_deletion) #For Deleting the User Profile from the Site Owner
    app.register_blueprint(order_status) #For Checking the Order Status

    return app