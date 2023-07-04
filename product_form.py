from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class SearchForm(FlaskForm):
    search_name = StringField('Product Name', validators=[Length(max=100)])
    search_submit = SubmitField('Submit')