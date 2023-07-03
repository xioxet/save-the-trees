from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField("Login")
    checkbox = BooleanField("Remember Me")

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password',validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired()])
    submit = SubmitField("Login")


class User:
    def __init__(self, user_id, username, password, email):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email

    def get_id(self):
        return self.username
    
users = {
    "username":"password"
}