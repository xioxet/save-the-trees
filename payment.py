from flask_wtf import FlaskForm
from wtforms import FileField, TextAreaField, IntegerField, StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, Regexp

# classes by v.
class PaymentForm_1(FlaskForm):
    payment_fname = StringField('First Name', validators=[DataRequired(), Length(min=0, max=45)])
    payment_lname = StringField('Last Name', validators=[DataRequired(), Length(min=0, max=45)])
    payment_quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1, max=100)])
    payment_message = TextAreaField('Write a Message', validators=[Length(max=200)])
    payment_anonymous = BooleanField('Remain Anonymous')
    payment_submit = SubmitField('Next')

class SatisfyForm(FlaskForm):
    order_submit = SubmitField('Mark')