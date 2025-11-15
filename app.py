import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, current_app, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from PIL import Image
import secrets 
from werkzeug.utils import secure_filename
from contextlib import contextmanager 
load_dotenv() 
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'my_default_secret_key_123') 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'lazy_blog.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Please log in to access this page."
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    password_hash = db.Column(db.String(200), nullable=False) 
    profile_image = db.Column(db.String(20), nullable=False, default='default_profile.png')
    security_question = db.Column(db.String(255), nullable=True)
    security_answer_hash = db.Column(db.String(200), nullable=True)
    recovery_token = db.Column(db.String(50), nullable=True, unique=True) 
    posts = db.relationship('Post', backref='author', lazy=True)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def set_security_answer(self, answer):
        self.security_answer_hash = generate_password_hash(answer)
    def check_security_answer(self, answer):
        if not self.security_answer_hash:
            return False
        return check_password_hash(self.security_answer_hash, answer)
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_file = db.Column(db.String(200), nullable=True, default='img/default_post_bg.png') 
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    filename = secure_filename(form_picture.filename) 
    _, f_ext = os.path.splitext(filename)
    picture_fn = random_hex + f_ext
    profile_pics_dir = os.path.join(app.root_path, 'static', 'img', 'profile_pics')
    os.makedirs(profile_pics_dir, exist_ok=True)
    picture_path = os.path.join(profile_pics_dir, picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
def save_post_picture(form_picture):
    random_hex = secrets.token_hex(8)
    filename = secure_filename(form_picture.filename) 
    _, f_ext = os.path.splitext(filename)
    picture_fn = random_hex + f_ext
    post_pics_dir = os.path.join(app.root_path, 'static', 'img', 'post_images')
    os.makedirs(post_pics_dir, exist_ok=True)
    picture_path = os.path.join(post_pics_dir, picture_fn)
    output_size = (800, 450)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return 'img/post_images/' + picture_fn
def delete_old_picture(old_picture_fn):
    if old_picture_fn != 'default_profile.png':
        old_picture_path = os.path.join(app.root_path, 'static/img/profile_pics', old_picture_fn)
        if os.path.exists(old_picture_path):
            os.remove(old_picture_path)       
def delete_old_post_picture(old_picture_fn):
    if old_picture_fn and old_picture_fn != 'img/default_post_bg.png':
        old_picture_path = os.path.join(app.root_path, 'static', old_picture_fn) 
        if os.path.exists(old_picture_path):
            os.remove(old_picture_path)
def construct_image_url(user):
    if user.profile_image == 'default_profile.png':
        return url_for('static', filename='img/' + user.profile_image)
    else:
        return url_for('static', filename='img/profile_pics/' + user.profile_image)
@app.route('/')
def index():
    all_posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html', posts=all_posts)
@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)
@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_image_file = 'img/default_post_bg.png' 
        if 'image_file' in request.files and request.files['image_file'].filename != '':
            image_file = request.files['image_file']
            if image_file.content_type.startswith('image/'):
                try:
                    post_image_file = save_post_picture(image_file)
                except Exception as e:
                    flash(f'Error processing image: {e}', 'danger')
                    return redirect(url_for('create_post'))
            else:
                flash('Uploaded file is not a valid image.', 'danger')
                return redirect(url_for('create_post'))

        new_post = Post(title=post_title, content=post_content, author=current_user, image_file=post_image_file)
        try:
            db.session.add(new_post)
            db.session.commit()
            flash('Your post has been published!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            if post_image_file != 'img/default_post_bg.png':
                delete_old_post_picture(post_image_file)  
            flash(f'An error occurred: {e}', 'danger')
            return redirect(url_for('create_post'))
    else:
        return render_template('create.html')
@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        if 'image_file' in request.files and request.files['image_file'].filename != '':
            image_file = request.files['image_file']
            if image_file.content_type.startswith('image/'):
                old_image_file = post.image_file
                try:
                    new_image_file = save_post_picture(image_file)
                    post.image_file = new_image_file
                    delete_old_post_picture(old_image_file)
                except Exception as e:
                    flash(f'Error processing new image: {e}', 'danger')
                    return redirect(url_for('edit_post', post_id=post.id))
            else:
                flash('Uploaded file is not a valid image.', 'danger')
                return redirect(url_for('edit_post', post_id=post.id))
        if 'remove_picture' in request.form and request.form['remove_picture'] == 'true':
            if post.image_file != 'img/default_post_bg.png':
                delete_old_post_picture(post.image_file)
                post.image_file = 'img/default_post_bg.png'
        post.title = post_title
        post.content = post_content
        try:
            db.session.commit()
            flash('Your post has been updated!', 'success')
            return redirect(url_for('post', post_id=post.id))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while updating your post: {e}', 'danger')
            return redirect(url_for('edit_post', post_id=post.id))
    else:
        return render_template('edit.html', post=post)
@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    try:
        delete_old_post_picture(post.image_file)
        db.session.delete(post)
        db.session.commit()
        flash('Your post has been successfully deleted!', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred while deleting your post: {e}', 'danger')
        return redirect(url_for('post', post_id=post.id))
@app.route('/search')
def search():
    query = request.args.get('q')
    results = []
    if query:
        results = Post.query.filter(
            db.or_(Post.title.ilike(f'%{query}%'), Post.content.ilike(f'%{query}%'))
        ).order_by(Post.date_posted.desc()).all()
    return render_template('search_results.html', query=query, results=results)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index')) 
    if request.method == 'POST':
        identifier = request.form['username_or_email']
        password = request.form['password']
        user = User.query.filter(db.or_(User.username == identifier, User.email == identifier)).first()   
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check username/email and password.', 'danger')
    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        security_question = request.form['security_question']
        security_answer = request.form['security_answer']
        if password != password_confirm:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))
        if not security_question or not security_answer:
            flash('Security question and answer are required.', 'danger')
            return redirect(url_for('register'))
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash('Username already taken.', 'warning')
            return redirect(url_for('register'))
        email_exists = User.query.filter_by(email=email).first()
        if email_exists:
            flash('Email address already in use.', 'warning')
            return redirect(url_for('register'))
        new_user = User(username=username, email=email, first_name=first_name, last_name=last_name)
        new_user.set_password(password)
        new_user.security_question = security_question
        new_user.set_security_answer(security_answer)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {e}', 'danger')
            return redirect(url_for('register'))
    else:
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        return render_template('register.html')
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been signed out.', 'success')
    return redirect(url_for('index'))
@app.route('/recover', methods=['GET', 'POST'])
def recover_password():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'find_user':
            username_or_email = request.form.get('username_or_email')
            user = User.query.filter(db.or_(User.username == username_or_email, User.email == username_or_email)).first()
            if user and user.security_question:
                # Found user, render STAGE 2
                return render_template('recover_password.html', 
                                       stage='answer', 
                                       question=user.security_question, 
                                       user_id=user.id)
            else:
                flash('User not found or no security question set.', 'danger')
                return redirect(url_for('recover_password'))
        elif action == 'reset_password':
            user_id = request.form.get('user_id')
            submitted_answer = request.form.get('submitted_answer')
            new_password = request.form.get('new_password')
            user = User.query.get(user_id) 
            if user and user.check_security_answer(submitted_answer):
                user.set_password(new_password)
                db.session.commit()
                flash('Password successfully reset! You can now sign in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Security answer was incorrect. Please try again.', 'danger')
                return render_template('recover_password.html', 
                                       stage='answer', 
                                       question=user.security_question, 
                                       user_id=user.id)
    return render_template('recover_password.html', stage='username', question=None)
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message_content = request.form['message']
        flash('Your message has been received.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')
@app.route('/profile')
@login_required
def profile():
    image_file = construct_image_url(current_user)
    return render_template('profile.html', user=current_user, image_file=image_file)
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        user = current_user
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.username = request.form['username']
        user.email = request.form['email']
        if 'profile_picture' in request.files and request.files['profile_picture'].filename != '':
            old_picture = current_user.profile_image
            picture_file = save_picture(request.files['profile_picture'])
            current_user.profile_image = picture_file
            if old_picture != 'default_profile.png':
                delete_old_picture(old_picture)
        if 'remove_picture' in request.form and request.form['remove_picture'] == 'true':
            if current_user.profile_image != 'default_profile.png':
                delete_old_picture(current_user.profile_image)
                current_user.profile_image = 'default_profile.png'
        try:
            db.session.commit()
            flash('Your profile has been updated!', 'success')
            return redirect(url_for('profile'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while updating your profile: {e}', 'danger')
            return redirect(url_for('edit_profile'))
    image_file = construct_image_url(current_user)
    return render_template('edit_profile.html', user=current_user, image_file=image_file)
@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user_to_delete = current_user
    email_address = user_to_delete.email
    username = user_to_delete.username
    for post in user_to_delete.posts:
        delete_old_post_picture(post.image_file) 
        db.session.delete(post)
    delete_old_picture(user_to_delete.profile_image)
    db.session.delete(user_to_delete)
    db.session.commit()
    logout_user()
    try:
        flash(f"Account for {username} successfully deleted.", 'success')
    except Exception as e:
        flash(f"An error occurred: {e}", 'warning')
    return redirect(url_for('index'))
@contextmanager
def app_context_scope():
    """Provides a transactional scope around app context."""
    with app.app_context():
        try:
            yield
        finally:
            pass 
with app_context_scope():
    db.create_all()