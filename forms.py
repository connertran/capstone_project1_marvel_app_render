from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Optional

class RegisterForm(FlaskForm):
    """Register Form"""

    username = StringField("Username", validators=[InputRequired(message="Username cannot be blank!")])
    password = PasswordField("Password", validators=[InputRequired(message="Enter your password!")])
    email = EmailField("Email", validators=[InputRequired(message="What is your email?")])
    first_name = StringField("First name", validators=[InputRequired(message="Enter your first name.")])
    last_name = StringField("Last name", validators=[InputRequired(message="Enter your last name.")])
    image_url = StringField("Image", validators=[Optional()])
    bio = StringField("Bio", validators=[InputRequired(message="Your bio is missing!")])

class LoginForm(FlaskForm):
    """Login Form"""
    username = StringField("Username", validators=[InputRequired(message="Username cannot be blank")])
    password = PasswordField("Password", validators=[InputRequired(message="Enter your password.")])

class EditForm(FlaskForm):
    """Edit Form for users to change their profile information"""

    username = StringField("Username", validators=[InputRequired(message="Username cannot be blank!")])
    email = EmailField("Email", validators=[InputRequired(message="What is your email?")])
    first_name = StringField("First name", validators=[InputRequired(message="Enter your first name.")])
    last_name = StringField("Last name", validators=[InputRequired(message="Enter your last name.")])
    image_url = StringField("Image", validators=[Optional()])
    bio = StringField("Bio", validators=[InputRequired(message="Your bio is missing!")])
    password = PasswordField("Password", validators=[InputRequired(message="Enter your password!")])

class PostForm(FlaskForm):
    """Post Form."""

    text = StringField("Text", validators=[InputRequired(message="Please enter your post text.")])