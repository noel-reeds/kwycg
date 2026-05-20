from flask import flash, Blueprint, render_template, request, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import User, db_engine as db


user_views = Blueprint('auth', __name__)


@user_views.route('/login')
def user_login():
    """Logs in a user into the app"""
    return render_template('login.html')

@user_views.route('/signup')
def user_signup():
    """Signs up a user"""
    return render_template('signup.html')

@user_views.route('/logout')
@login_required
def user_logout():
    """Logs out a user"""
    logout_user()
    return redirect(url_for('main.index'))
