import base64
import os
import werkzeug.exceptions
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app import app, login_manager
from .forms import CreatePostForm
from .models import db, User, Post, Like


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email address already exists')
            return redirect(url_for('register'))

        new_user = User(email=email, username=username, password_hash=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    user = current_user

    followed_users_ids = [f.followed_id for f in user.following.all()]
    followed_users_ids.append(current_user.id)

    # posts by followed users and me, sorted by last edit date or post date desc.
    posts = Post.query.filter(Post.user_id.in_(followed_users_ids)).order_by(Post.last_edited.desc().nullslast(),
                                                                             Post.timestamp.desc()).all()

    # posts by not followed users, sorted by last edit date or post date desc.
    posts += Post.query.filter(Post.user_id.notin_(followed_users_ids)).order_by(Post.last_edited.desc().nullslast(),
                                                                                 Post.timestamp.desc()).all()

    return render_template('dashboard.html', posts=posts)


@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        image = request.files[form.image_url.name]
        base64_encoded_image = None

        if image:
            filename = secure_filename(image.filename)
            file_ext = os.path.splitext(filename)[1].lower()

            if file_ext not in ['.jpg', '.jpeg', '.png', '.gif']:
                return 'Invalid file extension', 400

            base64_encoded_image = base64.b64encode(image.read()).decode('utf-8')

        if form.start_date.data == "":
            form.start_date.data = None

        if form.end_date.data == "":
            form.end_date.data = None

        post = Post(title=form.title.data, body=form.body.data, tags=form.tags.data, start_date=form.start_date.data,
                    end_date=form.end_date.data, user_id=current_user.id, geolocation=form.geolocation.data,
                    lat_lon=form.lat_lon.data,
                    image_url=base64_encoded_image)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('create_post.html', form=form)


@app.route('/profile', methods=['GET'])
@app.route('/profile/<int:user_id>', methods=['GET'])
@login_required
def profile(user_id=None):
    return render_template('profile.html', user=User.query.filter_by(id=user_id).first() if user_id else current_user)


@app.route('/follow/<user_id>', methods=['POST'])
@login_required
def follow(user_id):
    user_to_follow = User.query.filter_by(id=user_id).first()
    if user_to_follow is None:
        flash('User {} not found.'.format(user_id))
        return redirect(url_for('dashboard'))

    if current_user.is_following(user_to_follow):
        flash('You are already following {}.'.format(user_id))
        return redirect(url_for('profile', id=user_id))

    current_user.follow(user_to_follow)
    db.session.commit()
    flash('You are now following {}!'.format(user_id))
    return redirect(url_for('profile', user_id=user_id))


@app.route('/unfollow/<user_id>', methods=['POST'])
@login_required
def unfollow(user_id):
    user_to_unfollow = User.query.filter_by(id=user_id).first()
    if user_to_unfollow is None:
        flash('User {} not found.'.format(user_id))
        return redirect(url_for('dashboard'))

    if not current_user.is_following(user_to_unfollow):
        flash('You are not following {}.'.format(user_id))
        return redirect(url_for('profile', id=user_id))

    current_user.unfollow(user_to_unfollow)
    db.session.commit()
    flash('You are no longer following {}.'.format(user_id))
    return redirect(url_for('profile', user_id=user_id))


@app.route('/like_post/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify(success=False, message="Post not found"), 404

    like = Like(user_id=current_user.id, post_id=post.id)

    is_liked = db.session.query(Like).filter((Like.user_id == like.user_id) & (Like.post_id == post.id)).first()

    if is_liked:
        db.session.delete(is_liked)
    else:
        db.session.add(like)

    db.session.commit()

    return jsonify(success=True, message="Post liked", likes=post.likes.count())


@app.errorhandler(werkzeug.exceptions.Unauthorized)
def restricted(exception):
    return redirect(url_for('login'))


@app.route('/')
def index():
    return redirect(url_for('login'))
