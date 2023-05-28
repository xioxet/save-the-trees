from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length

class ContactForm(FlaskForm):
    contact_email = StringField('Email', validators=[DataRequired(), Email(), Length(max=255)])
    contact_fname = StringField('First Name', validators=[DataRequired(), Length(max=255)])
    contact_lname = StringField('Last Name', validators=[DataRequired(), Length(max=255)])
    contact_category = SelectField('Category', choices=[
        ('payment', 'Payment'),
        ('account', 'Account'),
        ('events', 'Events'),
        ('merchandise', 'Merchandise'),
        ('other', 'Other'),

    ])
    contact_message = TextAreaField('Write a message...', validators=[DataRequired(), Length(max=500)])
    contact_submit = SubmitField('Submit')

class ContactResponseForm(FlaskForm):
    contact_response = TextAreaField('Write a reply...', validators=[DataRequired()])
    contact_submit = SubmitField("Submit")

class ContactDeleteForm(FlaskForm):
    contact_submit = SubmitField("Delete")