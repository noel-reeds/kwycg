from . import db_engine as db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime as dt

class User(db.Model, UserMixin):
    """User model, defines a user and attrs"""

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)
    passwd_hash = db.Column(db.String(128), nullable=True)
    created_at = db.Column(dt.datetime.isoformat(dt.now()))
    
    # establish a relation between the user and expense table
    expenses = db.relationship('Expense', backref='user', lazy='dynamic')

    def __repr__(self):
        """prints a user object"""
        return '{} - {}'.format(self.name, self.email)
    
    def to_dict(self):
        """converts user object into a serializable object"""
        return dict(username=self.username,
                    passwd_hash=self.passwd_hash,
                    email=self.email,
                    id=self.id,
                    created_at=self.created_at
                )

    def hash_passwd(self, password):
        self.passwd_hash =  generate_password_hash(password)

    def verify_passwd(self, password):
        return check_password_hash(self.passwd_hash, password)
