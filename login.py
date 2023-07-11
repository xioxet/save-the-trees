from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField("Login")
    checkbox = BooleanField("Remember Me")


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=45)])
    password = StringField('Password', validators=[DataRequired(), Length(min=1, max=45)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=45)])
    submit = SubmitField("Login")


class User:
    def __init__(self, user_id, username, password, email, role):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.role = role

    def get_id(self):
        return self.username

