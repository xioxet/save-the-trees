from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange, Length

# classes by v.
class PaymentForm_1(FlaskForm):
    payment_email = StringField('Email', validators=[DataRequired(), Email()])
    payment_fname = StringField('First Name', validators=[DataRequired()])
    payment_lname = StringField('Last Name', validators=[DataRequired()])
    payment_message = TextAreaField('Write a Message')
    payment_anonymous = BooleanField('Remain Anonymous')
    payment_submit = SubmitField('Next')

class PaymentForm_2(FlaskForm):
    payment_cc_no = StringField('Credit Card Number', validators=[DataRequired(), Length(min=16, max=16)])
    payment_expiration_month = IntegerField('Expiration Month', validators=[DataRequired(), NumberRange(min=1, max=12)])
    payment_expiration_year = IntegerField('Expiration Year', validators=[DataRequired(), NumberRange(min=2023, max=2050)])
    payment_cvv = IntegerField('CVV', validators=[DataRequired(), NumberRange(min=100,max=999)])
    payment_billing_address_1 = StringField('Billing Address', validators=[DataRequired()])
    payment_billing_address_2 = StringField('', validators=[DataRequired()])
    payment_submit = SubmitField('Pay')