if not current_user.is_authenticated:
        flash("you need to login to book a slot","Warning")
        return redirect(url_for('auth.login'))

    if request.method == "POST":
        if form.validate_on_submit():
            print("Form is valid. Proceeding to save the booking.")
            existing_booking=CustomerBooking.query.filter_by(user_id=current_user.id,
                                                            service=form.service.data,
                                                            booking_time=form.booking_time.data).first()
            if existing_booking:
                flash("You have already booked this service at the same timing in our DataBase!","warning")
            else:
                print("Form validation failed.")
                print(form.errors)  # Print any validation errors
                #Booking our Orders
                booking=CustomerBooking(
                    user_id=current_user.id,
                    service=form.service.data,
                    booking_time=form.booking_time.data,
                    number_of_items=form.number_of_items.data,
                    delivery_area=form.delivery_area.data,
                    delivery_address=form.delivery_address.data,
                    mobile_number=form.mobile_number.data
                )
                print("Adding booking to the session.")
                try:
                    db.session.add(booking)
                    db.session.commit()
                    print("Booking saved Successfully!")
                except Exception as e:
                    print(f"Error Saving Successfully! {e}")
                    db.session.rollback() #Rollback the session in case of error.

                #Send confirmation Email:
                customer_email=current_user.email #email-id just pulled up from mnodels.py
                msg=Message("Booking Confirmation",
                            sender="scarywolf98@gmail.com",
                            recipents=[customer_email])
                msg.body = (
                    "Thanks for the booking. Your Booking ID is {}. "
                    "The site owner named Mani will call you to discuss this separately. "
                    "Please pick the call or you can make the call to this number +91 XXX XXX X XXX. "
                    "Thank you :(".format(booking.id)
                )
                mail.send(msg)

                flash("Your booking has been confirmed!","success")
                logging.debug("Redirecting to admin dashboard...") #
                return redirect(url_for("admin.admin_dashboard", id=current_user.id))  #Redirect to all Orders Page with the respective user ID's.
            
    #Render the Booking Form:
    return render_template("book_slot.html",form=form)


    ##################################### Full Logic behind a booking a form
    # 
    # #Customer Booking routes
#@csrf.exempt #Sometimes we can also use this exempt to avoid the csrf token verification
@book_slot.route("/booking_slots",methods=["GET","POST"])
@login_required

def slot_booking():
    form=CustomerBookingForm()  
    print("************************** Down Righ Here brotha! **************************")
    logging.debug(f"Current User ID: {current_user.id}")
    logging.debug("Redirecting to admin dashboard...")
    if request.method == "POST":
        if form.validate_on_submit():
            print("Form is valid. Proceeding to save the booking.")
            existing_booking = CustomerBooking.query.filter_by(
                user_id=current_user.id,
                service=form.service.data,
                #booking_time=form.booking_time.data
            ).first()

            if existing_booking:
                flash("You have already booked this service at the same timing in our DataBase!", "warning")
                return render_template("book_slot.html", form=form)  # Render the form again

            # Booking our Orders
            booking = CustomerBooking(
                user_id=current_user.id,
                service=form.service.data,
                number_of_items=form.number_of_items.data,
                delivery_area=form.delivery_area.data,
                delivery_address=form.delivery_address.data,
                mobile_number=form.mobile_number.data
            )
            print("Adding booking to the session.")
            try:
                db.session.add(booking)
                db.session.commit()
                saved_booking = CustomerBooking.query.filter_by(user_id=current_user.id, service=form.service.data).first()
                if saved_booking:
                    print("Booking saved successfully!")
                else:
                    print("Booking was not saved.")
            except Exception as e:
                print(f"Error Saving Successfully! {e}")
                db.session.rollback()  # Rollback the session in case of error.

            # Send confirmation Email
            # (Email sending logic remains unchanged)

            flash("Your booking has been confirmed!", "success")
            print(" ************************ Outputting Informations Here ************************ ")
            print("Form data:", form.data)  # Print the submitted form data
            return redirect(url_for("admin.admin_dashboard", id=current_user.id))  # Redirect to admin dashboard

        else:
            print("Form validation failed.")
            print(form.errors)  # Print any validation errors

    # Render the Booking Form
    return render_template("book_slot.html", form=form)



#models.py:
'''
#Models for Service-Type:
class ServiceType(db.Model):
    __tablename__ = 'service_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # Change the backref name to avoid conflict
    bookings = db.relationship("CustomerBooking", backref="service_type", lazy=True)

    # Represents the service type name
    #def __repr__(self):
    #    return f"<ServiceType: {self.name}>"
''' 

#This script is somewhere from the Site_Owner_Needed this to hear brotha.


@site_owner.route("/site_owner/login", methods=["GET", "POST"])
def login():
    form = SiteOwnerLoginForm()
    if form.validate_on_submit():
        # Fetch the owner based on the provided username
        owner = Website_Owner.query.filter_by(owner_name=form.ownername.data).first()
        
        # Check if the owner exists and if the password is correct
        if owner and owner.check_password(form.ownerpassword.data):
            if not owner.is_site_owner:  # Check if the user is not a site owner
                flash("Only site owners can access this section.", "danger")
                return redirect(url_for("auth.login"))  # Redirect to a suitable page
            
            login_user(owner)
            session["user_role"] = "owner"  # Set user role in session
            return redirect(url_for("site_owner.website_owner"))
        else:
            flash("Login Unsuccessful. Please check username and password.", "danger")
    
    return render_template("login.html", form=form)