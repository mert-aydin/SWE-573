from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired


class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    tags = StringField('Tags')
    start_date = StringField('Start Date', default=None)
    start_date_free = StringField('Start Date Free')
    end_date = StringField('End Date', default=None)
    end_date_free = StringField('End Date Free')
    geolocation = StringField('Geolocation', validators=[DataRequired()])
    lat_lon = StringField('lat_lon', validators=[DataRequired()])
    image_url = FileField('Image')
    submit = SubmitField('Submit')
