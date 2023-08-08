from flask_wtf import FlaskForm
from wtforms import FileField, TextAreaField, IntegerField, StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length


# classes by v.
class PaymentForm_1(FlaskForm):
    payment_fname = StringField('First Name', validators=[DataRequired()])
    payment_lname = StringField('Last Name', validators=[DataRequired()])
    payment_quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1, max=100)])
    payment_message = TextAreaField('Write a Message')
    payment_anonymous = BooleanField('Remain Anonymous')
    payment_submit = SubmitField('Next')

class SatisfyForm(FlaskForm):
    order_submit = SubmitField('Mark')