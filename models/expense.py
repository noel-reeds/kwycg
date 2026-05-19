import uuid
from models import database as db
from datetime import datetime, date
from flask import jsonify as js


class Expense(db.Model):
    """Entails details of an expenditure"""

    __tablename__ = 'expenses'

    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


    def __init__(self, *args, **kwargs):
        """Initializes expenses' ids"""
        self.id = str(uuid.uuid4())
        self.date = date.today()
        # check kwargs supplied for instance creation
        if kwargs:
            for key, value in kwargs.items():
                if value is None:
                    return js({"message": "attr {} cannot be None".format(key)})
        self.amount = kwargs.get('amount')
        self.category = kwargs.get('category')
        self.name = kwargs.get('name')
        self.desc = kwargs.get('desc')
        self.user_id = kwargs.get('user_id')
    
    def to_dict(self):
        """Returns a dictionary of the expense"""
        return dict(id=self.id,category=self.category,\
                    user_id=self.user_id,desc=self.desc,\
                    name=self.name,amount=self.amount,\
                    date=self.date.isoformat())
