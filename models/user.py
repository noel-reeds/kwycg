from . import database as db

class User(db.Model):
    """User model, defines a user and attrs"""

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    # establish a relation between the user and expense table
    expenses = db.relationship('Expense', backref='user', lazy='dynamic')

    def __repr__(self):
        """prints a user object"""
        return '{} - {}'.format(self.name, self.email)
    
    def to_dict(self):
        """converts user object into a serializable object"""
        return dict(id=self.id,name=self.name,email=self.email)
