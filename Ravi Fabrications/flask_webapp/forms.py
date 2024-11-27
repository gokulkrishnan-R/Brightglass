#Flask-Forms
"""from flask_form import Form
from flask_form.fields import StringField, PasswordField
from flask_form.validators import DataRequired, Email, EqualTo

class SignupForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])"""

#Flaskwtf-forms
from flask_wtf import FlaskForm  # Import FlaskForm instead of Form
from wtforms import Form, StringField, PasswordField, SubmitField,DateTimeField,BooleanField,IntegerField,TextAreaField,SelectField
from wtforms.validators import DataRequired, Email, EqualTo

#This is for Signup Form from WTF-Schema
class SignupForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('sign up')

#And  for Login Form from WTF-Schema
class LoginForm(FlaskForm):
    username=StringField("username",validators=[DataRequired()])
    #email=StringField("email",validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')  # Add this line
    submit = SubmitField('Log In')


#Logic for Updating the Forms
class UpdateForm(SignupForm):
    username = StringField(SignupForm.username, validators=[DataRequired()])
    email = StringField(SignupForm.email, validators=[DataRequired(), Email()])
    password = PasswordField(SignupForm.password, validators=[DataRequired()])
    submit = SubmitField('sign up')

#Forms for Quotesto Customer
class QuotesForm(FlaskForm):
    username=StringField("username",validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    service= StringField('service',validators=[DataRequired()])

#Forms for Service types they are looking for:

#Forms for CustomerBokking Services:
class CustomerBookingForm(FlaskForm):
    service = StringField('Service', validators=[DataRequired()])
    #service_type_id = SelectField('Service Type', choices=[('type1', 'Type 1'), ('type2', 'Type 2')], validators=[DataRequired()])  # Add this line
    number_of_items = IntegerField('Number of Items', validators=[DataRequired()])
    delivery_area = StringField('Delivery Area', validators=[DataRequired()])
    delivery_address = TextAreaField('Delivery Address', validators=[DataRequired()])
    mobile_number = IntegerField('Mobile Number', validators=[DataRequired()])
    #booking_time = DateTimeField('Booking Time', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    submit = SubmitField('Book Slot')

#PasswordReest form:
class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

#Form for PasswordResettng forms:
class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

#Site Owner Sign-up
class SiteOwnerSignupForm(FlaskForm):
    ownername = StringField("Owner Name", validators=[DataRequired()])
    ownerpassword = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")

#Site Owner Login
class SiteOwnerLoginForm(FlaskForm):
    ownername = StringField("ownername",validators=[DataRequired()])
    ownerpassword = PasswordField("ownerpassword",validators=[DataRequired()])

#Site_Owner change password form:
class ChangeCredentialsForm(FlaskForm):
    new_username = StringField("New Username", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired()])
    submit = SubmitField("Change Credentials!")

#Forms for Deleting the User Account.
class DeleteAccountForm(FlaskForm):
    submit = SubmitField('Delete Account')

 

#Job Links - 
  #https://in.indeed.com/viewjob?jk=9991421943e50dd7&q=python+developer&l=Ramanathapuram%2C+Coimbatore%2C+Tamil+Nadu&tk=1ice97loakfm6800&from=ja&alid=63d9272e47df04599eb7dc89&xpse=SoBu67I35QYdc2wkqp0LbzkdCdPP&xfps=5dd9a00b-9b10-4845-b39c-ce5f06dd395a&utm_campaign=job_alerts&utm_medium=email&utm_source=jobseeker_emails&rgtk=1ice97loakfm6800&xkcb=SoB367M35OaRAMbeV50GbzkdCdPP
  #https://in.indeed.com/viewjob?jk=9991421943e50dd7&q=python+developer&l=Ramanathapuram%2C+Coimbatore%2C+Tamil+Nadu&tk=1ice97loakfm6800&from=ja&alid=63d9272e47df04599eb7dc89&xpse=SoBu67I35QYdc2wkqp0LbzkdCdPP&xfps=5dd9a00b-9b10-4845-b39c-ce5f06dd395a&utm_campaign=job_alerts&utm_medium=email&utm_source=jobseeker_emails&rgtk=1ice97loakfm6800&xkcb=SoB367M35OaRAMbeV50GbzkdCdPP
  #https://mail.google.com/mail/u/0/#all/FMfcgzQXKDbxhSZwZZJBDGGZZHRsbDGX      