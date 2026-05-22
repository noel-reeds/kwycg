from flask import Blueprint, jsonify, g, request
from models import User, Expense, session, db_engine as db
from werkzeug.security import generate_password_hash
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

user = Blueprint('user', __name__)

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_passwd(password):
        return False
    g.user = user
    return True


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
        if not request.is_json:
            raise Exception
        updated = request.json
        user_id = g.user.id
        password = updated.get("password")
        if password is not None:
            pwd_hash = generate_password_hash(password)
            [updated.pop(k, None) for k in ['password', 'id']]
            updated.update(passwd_hash=pwd_hash)
            db.session.query(User).filter(User.id == g.user.id).update(updated)
            session.commit()
            return {"message": "OK"}
        else:
            updated.pop("id")
            db.session.query(User).filter(User.id == g.user.id).update(updated)
            session.commit()
            return {"message": "OK"}
    except Exception as e:
        return {"message": "FAILED"}
