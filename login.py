from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField("Login")
    checkbox = BooleanField("Remember Me")

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password',validators = [DataRequired()], widget=PasswordField())
    email = StringField('Email', validators = [DataRequired()])
    checkbox = BooleanField("Remember Me")


class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def get_id(self):
        return self.username


users = {}  # Placeholder for user data (in-memory storage)