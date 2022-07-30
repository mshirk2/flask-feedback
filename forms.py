from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length


class RegisterForm(FlaskForm):
    """Form to register user"""

    username = StringField("Username", validators=[
        InputRequired(message="Username is required")])
    
    password = PasswordField("Password", validators=[
        InputRequired(message="Password is required")])

    email = StringField("Email", validators=[
        InputRequired(message="Email is required")])

    first_name = StringField("First Name", validators=[
        InputRequired(message="First Name is required")])

    last_name = StringField("Last Name", validators=[
        InputRequired(message="Last Name is required")])


class LoginForm(FlaskForm):
    """Form for user login"""

    username = StringField("Username", validators=[
        InputRequired(message="Username is required")])
    
    password = PasswordField("Password", validators=[
        InputRequired(message="Password is required")])


class FeedbackForm(FlaskForm):
    """Add feedback form"""

    title = StringField("Title", validators=[InputRequired(), Length(max=50)])
    content = StringField("Content", validators=[InputRequired()])

class DeleteForm(FlaskForm):
    """Delete form - intentionally left blank"""