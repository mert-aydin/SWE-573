from datetime import datetime

from flask_login import UserMixin
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic', order_by=desc('timestamp'))
    following = db.relationship('Follower',
                                foreign_keys='Follower.follower_id',
                                backref=db.backref('follower', lazy='joined'),
                                lazy='dynamic')
    followers = db.relationship('Follower',
                                foreign_keys='Follower.followed_id',
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic')

    def follow(self, user):
        if not self.is_following(user):
            follow = Follower(follower_id=self.id, followed_id=user.id)
            db.session.add(follow)

    def unfollow(self, user):
        follow = self.following.filter_by(followed_id=user.id).first()
        if follow:
            db.session.delete(follow)

    def is_following(self, user):
        return self.following.filter_by(follower_id=self.id, followed_id=user.id).first()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(200))
    image_url = db.Column(db.String())
    geolocation = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    last_edited = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    likes = db.relationship('Like', backref='post', lazy='dynamic')
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def get_tags(self):
        if self.tags:
            return self.tags.split(';')

    def get_locations(self):
        if self.geolocation:
            return self.geolocation.split(';')

    def get_image(self):
        if self.image_url:
            return "data:image/png;base64," + self.image_url

    def is_liked(self):
        return self.likes.filter_by(user_id=current_user.id).first()


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    last_edited = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))


class Follower(db.Model):
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
