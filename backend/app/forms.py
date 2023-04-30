from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    tags = StringField('Tags')
    start_date = StringField('Start Date')
    end_date = StringField('End Date')
    geolocation = StringField('Geolocation')
    # image_url = StringField('Image URL')
    submit = SubmitField('Submit')
