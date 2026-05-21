from . import db_engine as db
from passlib.apps import custom_app_context as cac
from flask_login import UserMixin

class User(db.Model, UserMixin):
    """User model, defines a user and attrs"""

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)
    passwd_hash = db.Column(db.String(128), nullable=True)

    # establish a relation between the user and expense table
    expenses = db.relationship('Expense', backref='user', lazy='dynamic')

    def __repr__(self):
        """prints a user object"""
        return '{} - {}'.format(self.name, self.email)
    
    def to_dict(self):
        """converts user object into a serializable object"""
        return dict(id=self.id,name=self.name,email=self.email,
                    passwd_hash=self.passwd_hash)

    def hash_passwd(self, password):
        self.passwd_hash =  cac.hash(password)

    def verify_passwd(self, password):
        return cac.verify(password, self.passwd_hash)
