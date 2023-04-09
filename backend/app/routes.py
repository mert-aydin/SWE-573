from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, login_manager
from app.models import User, Post, Like


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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    if user.following.count() == 0:
        posts = Post.query.order_by(Post.last_edited.desc().nullslast(), Post.timestamp.desc()).all()
    else:
        followed_users_ids = [f.followed_id for f in user.following.all()]
        posts = Post.query.filter(Post.user_id.in_(followed_users_ids)).order_by(Post.last_edited.desc().nullslast(),
                                                                                 Post.timestamp.desc()).all()

    return render_template('dashboard.html', posts=posts)


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


@app.route('/')
def index():
    return redirect(url_for('login'))
