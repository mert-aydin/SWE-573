import humanize
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '****'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:******@/storyverse?host=/cloudsql/storyverse-385315:europe-central2:storyverse-2'  # app engine to cloud sql
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:******@34.118.67.200/storyverse' # local to cloud sql
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:******@localhost/storyverse' # local to local sql
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

from app import routes


@app.template_filter('relative_time')
def relative_time_filter(value):
    return humanize.naturaltime(value)


@app.template_filter('humanized_time')
def humanized_time_filter(value):
    return humanize.naturaldate(value)
