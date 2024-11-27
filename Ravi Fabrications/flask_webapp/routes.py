# Link for BLACKBOX CHAT AI - https://www.blackbox.ai/chat/Wm6J6xh.
# Customer restriction chat link - https://www.blackbox.ai/chat/Wm6J6xh
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, session, make_response
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, Order,Quotes,CustomerBooking,Website_Owner
from .forms import SignupForm, LoginForm,UpdateForm,QuotesForm,CustomerBookingForm,PasswordResetRequestForm,PasswordResetForm,SiteOwnerLoginForm,ChangeCredentialsForm,DeleteAccountForm,SiteOwnerSignupForm
from itsdangerous import URLSafeTimedSerializer #For password Reset Forms
from flask_mail import Message
from.import mail
import logging
import random
import string
from flask_mail import Message 
#from flask_weasyprint import HTML, render_pdf

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create Blueprints for different sections
main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)
admin = Blueprint("admin", __name__)
user_panel = Blueprint("user_panel", __name__)
user_signup = Blueprint("user_signup", __name__)
about_panel = Blueprint("about_panel", __name__)
profile_update_panel = Blueprint("profile_update_panel", __name__)
delete_orders = Blueprint("delete_orders", __name__)
book_slot = Blueprint("book_slot", __name__)
submit_quotation = Blueprint("submit_quotation", __name__)
forget_password=Blueprint("forget_password",__name__)
reset_password=Blueprint("reset_password", __name__)
site_owner=Blueprint("site_owner", __name__)
download_file=Blueprint("download_file", __name__)
delete_profile=Blueprint("delete_profile", __name__)
owner_profile_deletion = Blueprint("owner_profile_deletion", __name__)
order_status = Blueprint("order_status",__name__)
#generate_random=Blueprint("generate_random", __name__)

"""
# Mail_ID
def send_order_notification(order_id,customer_email):
    msg=Message("New Order Notification",
                recipients=["scarywolf98@gmail.com"])
    msg.body = f"A new order has been placed by {customer_email} with the Order ID {order_id}."
    mail.send(msg)
"""
    
# Function for Generating random Strings.
def random_ID():
    prefix = "BG"
    random_numbers = "".join(random.choices(string.digits, k=4)) #will make upto 4 digits
    return f"{prefix}-{random_numbers}"

# Public Routes (Like home, about, etc...)
@main.route("/")
def index():
    return render_template("index.html")

'''
# Download route:
@download_file.route("/booking_slots/download_file")
@login_required
def download_PDF():
    pass    
'''

#Route for Site-Owner Signup.
# Site Owner Signup Route
@site_owner.route("/site_owner/signup", methods=["GET", "POST"])
def site_owner_signup():
    form = SiteOwnerSignupForm()
    if form.validate_on_submit():
        # Check if the owner name already exists
        existing_owner = Website_Owner.query.filter_by(owner_name=form.ownername.data).first()
        if existing_owner:
            flash("Owner already exists! Please use a different name!", "danger")
            return redirect(url_for("site_owner.site_owner_signup"))

        # Create a new site owner
        new_owner = Website_Owner(
            owner_name=form.ownername.data,
            owner_password=generate_password_hash(form.ownerpassword.data)
        )
        db.session.add(new_owner)
        db.session.commit()
        flash("Site Owner account created successfully!", "success")
        return redirect(url_for("site_owner.login"))  # Redirect to login after signup

    return render_template("site_owner_signup.html", form=form)  # Render signup template


# Route for site owner dashboard
@site_owner.route("/site_owner/", methods=["GET", "POST"])
@login_required  # Ensure the user is logged in
def website_owner():
    # Check if the current user is the site owner
    #if current_user != current_user.is_site_owner:
    if not current_user.is_site_owner:   
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for('main.index'))  # Redirect to the main Index Page.
    
    #Order for Customers 
    orders = CustomerBooking.query.all()  # Fetch all bookings
    users = User.query.all() #Fetch all the booking Persons Name and Other Peoples name
    serivces = CustomerBooking.query.all()
    """if [orders,users] and current_user.is_authenticated:
        orders = CustomerBooking.query.all()  # Fetch all bookings
        users = User.query.all() #Fetch all the booking Persons Name and Other Peoples name


        #orders = CustomerBooking.query.all()  # Fetch all bookings
        db.session.delete(orders)
        db.session.delete(users)"""    

    return render_template("site_owner_dashboard.html", orders=orders,users=users,serivces=serivces)

# Owner login route
@site_owner.route("/site_owner/login", methods=["GET", "POST"])
def login():
    form = SiteOwnerLoginForm()
    if form.validate_on_submit():
        owner = Website_Owner.query.filter_by(owner_name=form.ownername.data).first()
        if owner and check_password_hash(owner.owner_password, form.ownerpassword.data):
            login_user(owner)
            session["user_role"] = "owner"  # Set user role in session
            return redirect(url_for("site_owner.dashboard"))  # Redirect to dashboard after login
        else:
            flash("Login Unsuccessful. Please check username and password.", "danger")

    return render_template("site_owner_dashboard.html", form=form)  # Render login template

# Dashboard route for site owner
@site_owner.route("/site_owner/dashboard", methods=["GET"])
@login_required
def dashboard():
    if not current_user.is_site_owner:
        flash("You do not have access to this section.", "danger")
        return redirect(url_for("main.index"))  # Redirect if not a site owner

    # Fetch orders or relevant data for the dashboard
    # Example: orders = Order.query.all()  # Adjust this query as necessary
    return render_template("dashboard.html")  # Render a dashboard template

#Route for Order Deletion by Site_Owner.
@owner_profile_deletion.route("/site_owner_deletion",methods=["POST"])
def owner_customer_order_deletion(id):
    if current_user.id == id:
        user = User.query.get_or_404(id)
        order = Order.query.get.filter_by(order)
        db.session.delete(user)
        db.session.commit()
        db.session.delete(order)
        db.session.commit()

#Route for checking the Order by OrderID.
@order_status.route("/status_check/",methods=["GET","POST"])
@login_required
def check_by_Order_id():
    users_2 = User.query.all()
    orders_2 = Order.query.all()
    serivces_2 = CustomerBooking.query.all()

    return render_template("Customer_Order_Check_ID.html", orders_2=orders_2,users_2=users_2,serivces_2=serivces_2)

"""
@delete_profile.route("/delete_profile/<int:id>/", methods=["POST"])
@login_required
def delete_account(id):
    if current_user.id == id:
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        logout()
        flash("Your account has been deleted successfully.", "success")
        return redirect(url_for("main.index"))  # Redirect to the home page
    else:
        flash("You cannot delete this account!", "danger")
        return redirect(url_for("main.index"))
"""    


# Route for changing credentials for Site Owner
@site_owner.route("/site_owner/change_credentials", methods=["GET", "POST"])
@login_required  # Ensure the user is logged in
def change_credentials():
    form = ChangeCredentialsForm()
    if form.validate_on_submit():
        current_user.owner_name = form.new_username.data
        current_user.set_password(form.new_password.data)  # Assuming you have a method to hash the password
        db.session.commit()
        flash("Credentials updated successfully!", "success")
        return redirect(url_for("site_owner.website_owner"))
    return render_template("change_credentials.html", form=form)

#Route fof Site Owner Logout:
@login_required
def logout():
    logout_user()
    session.pop("user_role", None) # Remove user role from session
    return redirect(url_for("main.index"))

# https://www.msys2.org/dev/python/
# https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation
# https://www.geeksforgeeks.org/how-to-create-pdf-files-in-flask/

# User Registration Route:
@user_signup.route("/signup", methods=["GET", "POST"])
def user_register():
    form = SignupForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please use a different username.", "danger")
            return redirect(url_for("user_signup.user_register"))

        # Hash the password and create a new user
        hashed_password = generate_password_hash(password) 
        user = User(username=username, email=email, password=hashed_password)
        
        db.session.add(user)
        db.session.commit()
        flash("Account Created Successfully!")
        return redirect(url_for("auth.login"))

    return render_template("signup.html", form=form)

# User authentication routes
@auth.route("/login", methods=["GET", "POST"])
def login():    
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data #Getting the value remember from the checkbox

        user = User.query.filter_by(username=username).first()
        #print(f"Stored hashed password: {user.password}")
        #print(f"Entered password: {user.password}")
        value1,value2=["scrypt:32768:8:1$y1lZzZ4QsLLKJXVO$0e0bddd56e42ed81ea40dda4c0406f80bf1110321977f591050b68ffa242d0a24f502b04f7f4b0df6def7d27dd04201e5495973c34fa2265afc5733079fa0df0",
                       "scrypt:32768:8:1$y1lZzZ4QsLLKJXVO$0e0bddd56e42ed81ea40dda4c0406f80bf1110321977f591050b68ffa242d0a24f502b04f7f4b0df6def7d27dd04201e5495973c34fa2265afc5733079fa0df0"
                    ]
        if value1 == value2:
            print("True, both are same")
        else:
            print("Nope, Both are differen!")

        if user is None:
            flash("You are not a member. Please sign up to login.", "warning")
            return redirect(url_for('user_signup.user_register'))
        
        # Check if the password matches
        if user.check_password(password): 
            login_user(user,remember=remember) #Passing our remember value
            flash("Login successful!", "success")
            return redirect(url_for("main.index"))
        else:
            flash("Invalid password. Please try again.", "danger")
            
    return render_template("login.html", form=form, user=current_user)

# User logout route
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))

# Admin(User indiviaul i,e. Customers) routes
@admin.route("/admin/<int:id>")
@login_required
def admin_dashboard(id):
    user = User.query.get_or_404(id)  # Fetch the user by ID
    orders = CustomerBooking.query.filter_by(user_id=user.id).all()  # Fetch orders for the specific user
    form = DeleteAccountForm()

    print(f"Orders for user {user.id}: {orders}")  # Debugging line

    return render_template("user_admin.html", user=user, orders=orders, form=form)  # Render the admin panel for order management
    """
    if not current_user.is_authenticated:
        flash("You need to login to access this page","warning")
        return redirect(url_for("auth.login"))
    
    #Fetch orders for the current user
    user = User.query.get_or_404(id)
    orders = CustomerBooking.query.filter_by(user_id=user.id).all()  # Fetch orders for the specific user
    update_profile = True
    if update_profile:
        flash("you have updated your Profile Successfully!","success")
    else:
        flash("Wrong datas Feed In.","danger")
    return render_template("user admin.html",user=user,orders=orders)  # Admin panel for order management
    """

# Deleting Particular Order Functionality:




#User Profile Update Route
@profile_update_panel.route("/profile_update_panel/<int:id>",methods=["GET","POST"])
def update_profile(id):
    # Fetch the user object from the database 
    user=User.query.get_or_404(id) 
    # Initialize the form with existing user data
    form=UpdateForm(obj=user)
    if form.validate_on_submit():
        # Update user attributes with form data
        user.username=form.username.data
        user.email=form.email.data
        # Only update password if provided
        if form.password.data:
            user.password=generate_password_hash(form.password.data)        
        db.session.commit()
        flash("Profile Update Successfully!","Success")
        return redirect(url_for("admin.admin_dashboard",id=user.id))  

    return render_template("all_profile_update.html",form=form)

#Customer Booking routes
#@csrf.exempt #Sometimes we can also use this exempt to avoid the csrf token verification
@book_slot.route("/booking_slots", methods=["GET", "POST"])
@login_required
def slot_booking():
    form = CustomerBookingForm()
    #orders = CustomerBooking.query.filter_by(user_id=user.id).all()  # Fetch orders for the specific user  
    logging.debug(f"Current User ID: {current_user.id}")

    if request.method == "POST":
        #Fetch the UserName from the DB.
        user=User.query.all()
        if form.validate_on_submit():
            logging.debug("Form is valid. Proceeding to save the booking.")
            # Generate a random order ID for the new booking
            order_id = random_ID()

            # Create a new booking without considering the service type
            booking = CustomerBooking(
                user_id=current_user.id,
                order_id=order_id,  # Set the generated order ID here
                service=form.service.data,  # Placeholder service name
                number_of_items=form.number_of_items.data,
                delivery_area=form.delivery_area.data,
                delivery_address=form.delivery_address.data,
                mobile_number=form.mobile_number.data
            )

            try:
                db.session.add(booking)
                db.session.commit()
                logging.debug("Booking saved successfully!")

                # *** Need to Check this part as this is not working anymore ***
                # Send email notification to the owner
                #send_order_notification(order_id, current_user.email)  # Assuming current_user has an email attribute

                flash("Your booking has been confirmed!", "success")
                return redirect(url_for("admin.admin_dashboard", id=current_user.id))
            except Exception as e:
                logging.error(f"Error saving booking: {e}")
                db.session.rollback()
                flash("An error occurred while saving your booking. Please try again.", "danger")
                return render_template("book_slot.html", form=form)
        else:
            logging.debug("Form validation failed.")
            logging.debug(form.errors)

    return render_template("book_slot.html", form=form)

#Email-Notifcation 
def send_order_notification(order_id, customer_email):
    msg = Message("New Booking Notification",
                  recipients=["owner_email@gmail.com"])  # Owner's email address
    msg.body = f"A new booking has been placed by {customer_email} with Order ID: {order_id}."
    mail.send(msg)

#Order delete routes
@delete_orders.route("/delete_order/<int:id>", methods=["POST"])
@login_required
def delete_customer_order(id):
    order = CustomerBooking.query.get(id)
    print("CSRF Token:", request.form.get('csrf_token'))
    if order:
        print(f"Order found: {order.id}, User ID: {order.user_id}, Current User ID: {current_user.id}")
    else:
        print("Order not found.")

    #if order and order.user_id == current_user.id:
    if order:
        db.session.delete(order)
        db.session.commit()
        flash("Order deleted successfully.", "success")
    else:
        flash("Order not found or you do not have permission to delete this order.", "danger")
    
    return redirect(url_for('admin.admin_dashboard', id=current_user.id))

'''
    # Delete the order
    db.session.delete(order)
    db.session.commit()
'''
    

"""
#Routes for submitting Quotation
@submit_quotation.route("/submit_quotations",methods=["POST","GET"])
#@login_required
def all_quotations(id):
    form=QuotesForm.query.filter_by_id_or_404(id=id)
    if form.validate_on_submit():
        username=form.name.data
        email=form.email.data

        # Check if the username already signedin for debugging purposes
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("You are already a Registered user. Please LOGIN and place the Order.", "danger")
        
        user = User(username=username, email=email)    
        db.session.add(user)
        db.session.commit()
        
    return render_template("quotations.html")
"""
#Routes for submitting Quotation
@submit_quotation.route("/submit_quotation/",methods=["POST","GET"])
@login_required
def all_quotations():
    # Fetch quotations for the current user
    quotations=Quotes.query.filter_by(user_id=current_user.id).all()
    return render_template("quotations.html",quotations=quotations)
        
#Route for Forgetting_passwords:
@forget_password.route("/reset_password",methods=["GET","POST"])
def reset_password_request():
    #forget_password.logger.debug("/reset_password")
    form=PasswordResetRequestForm()
    is_reset_page = True  # Indicate that we are on the reset password page
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            # Generate a password reset token
            s=URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
            token=s.dumps(user.email,salt="password-rest-salt")
            reset_url=url_for("reset_password",token=token,_external=True)

            #Sending Email:
            msg=Message("Password Reset Request",recipients=[user.email])
            msg.body = f"Please click the link to reset your password:{reset_url}"
            mail.send(msg)

            flash('An email has been sent with instructions to reset your password.', 'info')
        else:
            flash('No account found with that email address.', 'warning')
        return redirect(url_for("login"))
    return render_template('reset_password_request.html', form=form, is_reset_page=is_reset_page)

#Routes for Resettmng_Password
@reset_password.route("/reset_password/<token>",methods=["GET","POST"])
def reset_passwords(token):
    #reset_password.logger.debug("/reset_password/<token>")
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    email = s.loads(token, salt='password-reset-salt', max_age=3600)  # Token expires in 1 hour
    is_reset_page = True  # Indicate that we are on the reset password page
    print(f"is_reset_page: {is_reset_page}")
    form = PasswordResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=email).first()
        if user:
            user.set_password(form.password.data)
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('login'))
        return render_template("reset_password.html",form=form,is_reset_page=is_reset_page)

# User dashboard route
@user_panel.route("/dashboard")
@login_required
def user_dashboard():
    user_id=current_user.id #Get the current user's ID
    #orders = Order.query.filter_by(user_id=current_user.id).all()
    # You can also access roles or other user-related data if you have them
    return render_template("customer_orders.html", user_id=user_id)

# About page route
@about_panel.route("/about")
def about_page():
    return render_template("About Us.html")


#Function for deleting a User profile
@delete_profile.route("/delete_profile/<int:id>/", methods=["POST"])
@login_required
def delete_account(id):
    if current_user.id == id:
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        logout()
        flash("Your account has been deleted successfully.", "success")
        return redirect(url_for("main.index"))  # Redirect to the home page
    else:
        flash("You cannot delete this account!", "danger")
        return redirect(url_for("main.index"))