#Defining all Models  and Databases here
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
#from your_database_setup import Base  # Adjust the import based on your setup

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'users'  # Ensure consistent table name

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    #is_admin = db.Column(db.Boolean, default=False)  # False for CUSTOMERS, True for ADMIN
    orders = db.relationship('Order', backref='user', lazy=True)
    role = db.Column(db.String(50), nullable=False, default='customer')  # Default role is 'customer'

    # Method to set hashed password
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Method to check password
    def check_password(self, password):
        return check_password_hash(self.password, password)

    # Flask-Login requires these properties
    @property
    def is_authenticated(self):
        return True  # This user is authenticated

    @property
    def is_active(self):
        return True  # This user is active

    @property
    def is_anonymous(self):
        return False  # This user is not anonymous
    
    def get_id(self):
        return str(self.id)  # Return the user's ID as a string
    
    @property
    def is_site_owner(self):
        return self.role == "site.owner" #For site Owner
    
    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def is_site_owner(self):
        return self.role == 'site_owner' 

    def __repr__(self):
        return f'<User {self.username}>'
'''    
#model for service 
class ServiceType(db.Model):
    __tablename__ = 'service_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    bookings = db.relationship('CustomerBooking', backref='service_type_ref', lazy=True)
'''

# Model class for storing the Booking Details of Customer
class CustomerBooking(db.Model):
    __tablename__ = 'customer_bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    #service_type_id = db.Column(db.Integer, db.ForeignKey('service_types.id'), nullable=False)
    order_id = db.Column(db.String(20), unique=True, nullable=False)
    service = db.Column(db.String(120), nullable=False)  # Placeholder for service
    number_of_items = db.Column(db.Integer, nullable=False)
    delivery_area = db.Column(db.String(100), nullable=False)
    delivery_address = db.Column(db.String(200), nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False)
    status = db.Column(db.String(50), default='pending')

    user = db.relationship("User", backref="bookings")
    #service_type = db.relationship("ServiceType", backref="customer_bookings", lazy=True)

    def __repr__(self):
        return f"<Booking {self.id} - {self.service}>"


# Customer Database for Booking Orders
class Order(db.Model):

    __tablename__ = 'orders'  # Correct table name

    id = db.Column(db.Integer, primary_key=True)
    order_details = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Foreign key to User table
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for order creation
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp for updates

    def __repr__(self):
        return f'<Order {self.id} by User {self.user_id}>'

# Database storage for Customer Quotes
class Quotes(db.Model):

    __tablename__ = "customer_quotes"  # Consistent table name format

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Add this line
    user_name = db.Column(db.String(120), nullable=False)
    user_email = db.Column(db.String(120), nullable=False)
    user_service = db.Column(db.String(120), nullable=False)

    #Database Relationship 
    user = relationship("User", backref="quotes")  # Add this line for relationship

    def __repr__(self):
        return f'<Quote by {self.user_name} for service {self.user_service}>'
    

#Website Owner setup for authentication:
class Website_Owner(db.Model):
    
    __tablename__ = "site_owner"
    
    id = db.Column(db.Integer, primary_key=True)
    #site_owner_id = db.Column(db.Integer, db.ForeignKey('site_owner'))
    owner_name=db.Column(db.String(120),nullable=False)
    owner_password=db.Column(db.String(120),nullable=False)
    is_site_owner = db.Column(db.Boolean, default=True)  # Flag to indicate if this user is the site owner  

    def __repr__(self):
        return f"<Owner name is:{self.owner_name} and Owner password {self.owner_password}>"
    
    def set_password(self,password):
        self.owner_password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.owner_password,password)

#Absolutely! Whenever you refer to "Retrieve Details by Order_ID, to get in the details of the Orders.
