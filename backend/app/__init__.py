import os
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
import humanize
from datetime import datetime
from .models import db, User, Post, Like, Comment, Follower

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_APP_SECRET_KEY')
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{os.environ.get("POSTGRESQL_DB_PASSWORD")}@localhost/storyverse'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

from app import routes, models


@app.template_filter('relative_time')
def relative_time_filter(value):
    return humanize.naturaltime(value)


@app.template_filter('humanized_time')
def humanized_time_filter(value):
    return humanize.naturaldate(value)


if __name__ == '__main__':
    app.run(debug=True)
