from flask_wtf import FlaskForm
from wtforms import FileField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length

class ReviewForm(FlaskForm):
    rating = IntegerField('Rating (out of 5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField('Comment', validators=[DataRequired(), Length(min=1, max=500)])
    image = FileField('Image')