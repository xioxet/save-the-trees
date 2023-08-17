from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Login")
    checkbox = BooleanField("Remember Me")


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(message="Invalid email address")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField("Sign Up")

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Update")
    back = SubmitField("Back")

class VerificationForm(FlaskForm):
    verification_pin = StringField('Verification Code', validators=[DataRequired()])
    submit = SubmitField('Verify')

class DeleteForm(FlaskForm):
    delete = SubmitField('Verify')
    go_back = SubmitField('Go Back')

class DelVerification(FlaskForm):
    del_verification_pin = StringField('Verification Code', validators=[DataRequired()])
    delete = SubmitField('Delete Account')

class ForgotPasswordForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class User:
    def __init__(self, user_id, username, password, email, role, last_login_time=None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.role = role
        self.last_login_time = last_login_time

    def get_id(self):
        return self.user_id

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password
