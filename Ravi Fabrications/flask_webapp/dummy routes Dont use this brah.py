from flask import Blueprint, render_template, redirect, url_for, request,flash,session
from flask_login import login_user, logout_user, login_required, current_user,LoginManager,UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
#from . import db
from . models import db,User,Order
from .forms import SignupForm,LoginForm
from flask_wtf.csrf import generate_csrf
import time
 
# Create Blueprints for different sections
main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)
admin = Blueprint("admin", __name__)
user_panel=Blueprint("user_panel", __name__)
user_signup=Blueprint("user_signup",__name__)
about_panel=Blueprint("about_panel",__name__)

"""# Setup Flask-Login inside routes.py
login_manager=LoginManager()

# A simple user class without a database
class User(UserMixin):
    def __init__(self,id):
        self.id=id

# Mock user data (Replace this with a database later)
users={
    "1":User(1)
}"""

"""@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id) #Load user from the dummy users dict

@main.route('/login')
def login():
    user = users['1']  # Mock login for user with ID '1'
    login_user(user)
    return redirect(url_for('main.index'))

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return "You are now logged out!"
"""
# Public routes (like home, about, etc..)
@main.route("/")
def index():
    return render_template("index.html")

#This is for signing up for first time user routes
@user_signup.route("/signup", methods=["GET", "POST"])
def user_register():
    form = SignupForm()
    
    if form.validate_on_submit():
        # Process the form data
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Check if the email already exists
        existing_user=User.query.filter_by(username=username).first()
        if existing_user:
            flash("Email address already exists. Please use a different email.", "danger")
            return redirect(url_for("user_signup.user_register"))
        
        # Hash the password
        # Setting a hashed variable and calling DB retrieval options
        hashed_password = generate_password_hash(password) 

        # Create a new user
        user = User(username=username, email=email, password=hashed_password) #Called here for direct retrival.
        #user.set_password(form.password.data) #Hashing the password
        db.session.add(user)
        db.session.commit()
        db.session.close()

        flash("Account Created Successfully!")
        return redirect(url_for("auth.login"))  # Redirect to login page after signup

    return render_template("signup.html", form=form)  # CSRF is auto-injected in template
    
    """if request.method == "POST":
        username=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("password")

        #Checking if user already exists:
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Emal already Exists","danger")
            return redirect(url_for("auth.login"))
        #Hashing the new password and creating the new user:
        hashed_password=generate_password_hash(password,method="sha256")
        new_user=User(username=username,email=email,password=hashed_password)

        #saving the user to the databases
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registartion Successfull! Please log in","success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            db.session.rollback() #Rolling back from DB incase of any error
            flash("An error occurred while creating your account. Please try again.", "danger")
            print(f"Error{e}") #Log the error for debugging.
    else:
        return render_template("signup.html") """

# User authentication routes
@auth.route("/login", methods=["GET", "POST"])
def login():    

    form = LoginForm()

    if form.validate_on_submit():  # Make sure the form is submitted correctly
        #username = form.username.data.strip()
        #password = form.password.data.strip()
        username = form.username.data
        password = form.password.data

        # Fetch the user from the database by their email
        user = User.query.filter_by(username=username).first()

        # Print statements for debugging
        import sys
        print(f"Username: {username}",file=sys.stdout)  # Check the captured username
        print(f"Password: {password}",file=sys.stdout)  # Check the captured password
        print(f"Entered password: {password}",file=sys.stdout)
        #For debugging purposes
        value1="scrypt:32768:8:1$7wZszet9rnZFufYb$f97ece644a974773a6872a3323d068a1bc799729cf878992dcb057e305714b2e68e2ad3471a8c758d6a155ccdb7c898d56cca884fb00984b5196d9c3e96afcac"
        value2="scrypt:32768:8:1$7wZszet9rnZFufYb$f97ece644a974773a6872a3323d068a1bc799729cf878992dcb057e305714b2e68e2ad3471a8c758d6a155ccdb7c898d56cca884fb00984b5196d9c3e96afcac"
        if value1 == value2:
            print(True,"Yes, they are equal!")
        else:
            print("They are not equal!")

        # Check if the user exists in the database
        if user is None:
            flash("You are not a member. Please sign up to login.", "warning")
            return redirect(url_for('user_signup.user_register'))  # Redirect to signup if user not found
        
        # Check if the password matches (we are assuming you are hashing it correctly)
        #check_password=check_password_hash(user.password)
        if user.check_password(password):  # Correct email and password
            login_user(user)
            flash("Login successful!", "success")  # Success message for valid login
            print(f"Password match: {user.check_password(password)}")
            return redirect(url_for("main.index"))  # Redirect to the homepage
            

        else:
            # If email exists but password is wrong
            print("Password does not match.")
            print(f"Stored password hash: {user.password}")  # Print the stored hash for debugging
            flash("Invalid password. Please try again.", "danger")
    #elif user == logout:  
    
    return render_template("login.html",form=form,user=current_user)  # Render the login page if not submitted

# Individual Panel Routes
#@user_panel.route("/user_panel",methods=["GET"])
#def individual_user_panel():
# pass

#routes for first time user and unauthorized users
@auth.route("/login")
def unauthorized():
    flash ("You are unathrized! Please signup and loginto the website!")
    return redirect(url_for('user_signup.user_register'))


@auth.route("/logout")
@login_required
def logout():
    logout_user()  # Ensure to log out the user
    return redirect(url_for("main.index"))  # Redirecting to the main index

# Admin routes
@admin.route("/admin")
#@login_required
def admin_dashboard():
    # Only admin users can access
    if admin == False:
        #flash('Unauthorized Access!', 'danger')
        #return redirect(url_for("main.index"))
        return render_template("index.html")
    else:
        return render_template("dashboard.html")  # Admin panel for order management

# User-Admin routes
@user_panel.route("/user")
#@login_required
def user_dashboard():
    #if current_user.is_admin():
        #flash('Unauthorized Access!', 'danger')
        #return redirect(url_for("admin.admin_dashboard"))
    #return render_template('user admin.html')  # User panel for order management
    if not current_user.is_authenticated():
        flash("Please log in to view your orders.","danger")
        return redirect("auth.login")
    #Query to get the current user orders:
    orders=Order.query.filter_by(user_id=current_user.id).all()

    return render_template("customer_orders.html",orders=orders)

#About page route
@about_panel.route("/about")
def about_page():
    return render_template("About Us.html")
