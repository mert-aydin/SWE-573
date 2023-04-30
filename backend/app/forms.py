from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired


class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    tags = StringField('Tags')
    start_date = StringField('Start Date', validators=[DataRequired()])
    end_date = StringField('End Date', validators=[DataRequired()])
    geolocation = StringField('Geolocation', validators=[DataRequired()])
    image_url = FileField('Image')
    submit = SubmitField('Submit')
