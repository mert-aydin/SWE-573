import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_APP_SECRET_KEY')
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{os.environ.get("POSTGRESQL_DB_PASSWORD")}@localhost/storyverse'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from app import routes, models

if __name__ == '__main__':
    app.run(debug=True)
