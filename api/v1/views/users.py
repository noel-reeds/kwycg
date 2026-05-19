from flask import flash, Blueprint, render_template, request, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import User, db


user = Blueprint('user', __name__)

@user.route('/api/v1/users', methods=['GET'])
def users():
    """Retrieves all users in databases"""
    try:
        users = User.query.all()
        if users:
            return jsonify([user.to_dict() for user in users])
        else:
            return jsonify({'message':'no users'})
    except Exception as err:
        return jsonify({'message':'{}'.format(err)})

@user.route('/api/v1/user/<int:user_id>', methods=['GET'])
def specific_user(user_id):
    """Returns a specific user if present"""
    # check for a user matching the supplied id
    try:
        user = User.query.filter_by(id=user_id).first()
        return jsonify(user.to_dict())

    except Exception as err:
        return jsonify({'message':'user does not exist'})
