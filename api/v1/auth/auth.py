from flask import flash, Blueprint, render_template, request, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import User


auth = Blueprint('auth', __name__)


@auth.route('/login')
def user_login():
    """Logs in a user into the app"""
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login():
    """Redirects successful logins"""
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()

    """Check if user already exists, password check"""
    if user and check_password_hash(user.password, password):
        login_user(user)
        return redirect(url_for('main.profile'))
    
    """if check fails, return to login"""
    flash('Failed, check your credentials and try again')
    return redirect(url_for('auth.user_login'))

@auth.route('/signup')
def user_signup():
    """Signs up a user"""
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def user_logout():
    """Logs out a user"""
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/update_user', methods=['POST'])
@login_required
def update_user():
    """updates user info"""
    pass

@auth.route('/reset_password', methods=['PUT'])
def reset_password():
    """Resets user password"""
    password_info = request.json
    email = password_info.get('email')
    password = password_info.get('password')

    user = User.query.filter_by(email=email).first()
    if user:
        hash_password = generate_password_hash(password, method='pbkdf2:sha256')
        if check_password_hash(user.password, password):
            return jsonify({'message': 'provide a newer password'})
        user.password = hash_password
        return jsonify({'message': 'password reset success'})

    redirect(url_for('auth.user_signup'))
    return jsonify({'message': 'email does not exist, register to proceed'})
