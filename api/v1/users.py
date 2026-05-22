from flask import flash, Blueprint, render_template, request, redirect, url_for, jsonify
from models import User, Expense, session, db_engine as db
from passlib.apps import custom_app_context as cac
from .auth import auth

user = Blueprint('user', __name__)

@user.route('/users', methods=['GET'])
def users():
    """Retrieves all users in databases"""
    try:
        users = User.query.all()
        if users:
            return [user.to_dict() for user in users]
        else:
            return jsonify({'message':'no users'})
    except Exception as err:
        return jsonify({'message':'{}'.format(err)})

@user.route('/user/<int:user_id>', methods=['GET'])
async def specific_user(user_id):
    """Returns a specific user if present"""
    # check for a user matching the supplied id
    try:
        user = User.query.filter_by(id=user_id).first()
        return user.to_dict()

    except Exception as e:
        return jsonify({'message':'user does not exist'})

@user.route('/signup', methods=['POST'])
async def create_user():
	try:
		if request.is_json:
			user_creds = request.json
			password = user_creds.get("password")
		new_user = User(email=user_creds.get('email'),
						username=user_creds.get('username'),
						name=user_creds.get('name')
					)
		email=user_creds.get('email')
		user = User.query.filter_by(email=email).first()
		if user:
			return jsonify({'message': 'user already exists'})
		new_user.hash_passwd(password)
		session.add(new_user)
		session.commit()
		return jsonify({'message': 'OK'})
	except Exception as e:
		print(e)
		return jsonify({'message':'an error with the request'})

@user.route('/delete_a_user/<int:user_id>', methods=['DELETE'])
async def delete_a_user(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
        if user:
            session.delete(user)
            session.commit()
            return {"status": "OK"}
        return {"message": "user does not exist!"}
    except Exception as e:
        return {"message": "An error with the request!"}

@user.route('/update', methods=['UPDATE'])
@auth.login_required
def user_update():
    try:
        if request.is_json:
            updated = request.json
        user = User.query.filter_by(id=updated.get('id')).first()
        password = updated.get("password")
        if user and password in updated.keys():
            pwd_hash = cac.hash(password)
            [updated.pop(key) for key in ["id", "password"]]
            updated.update(passwd_hash=pwd_hash)
            db.session.query(User).update(updated)
            session.commit()
            return {"message": "OK"}
        elif user and password is None:
            updated.pop("id")
            db.session.query(User).update(updated)
            session.commit()
            return {"message": "OK"}
        raise Exception
    except Exception as e:
        return {"message": "FAILED"}
