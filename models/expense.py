from sqlalchemy import DateTime, Integer, Column, String, ForeignKey
from datetime import datetime, date
from flask import jsonify as js
from models import Base
from sqlalchemy.sql import func
import uuid

class Expense(Base):
    """
    Defines expenditure class, initialization and a
    to_dict function for serialization.
    """
    __tablename__ = 'expenses'

    id = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_accounts.id'), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)
    name = Column(String(50), nullable=False)
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


    def __init__(self, *args, **kwargs):
        """
        Initializes expenses' ids
        """
        self.id = str(uuid.uuid4())
        if kwargs:
            self.amount_spent = kwargs.get('amount')
            self.category = kwargs.get('category')
            self.name = kwargs.get('name')
            self.description = kwargs.get('description')
            self.user_id = kwargs.get('user_id')
    
    def to_dict(self):
        """
        Returns a dictionary of the expense
        """
        return dict(id=self.id,
                    category=self.category,
                    user_id=self.user_id,
                    description=self.description,
                    name=self.name,
                    amount_spent=self.amount_spent,
                    created_at=self.created_at,
                    updated_at=self.updated_at
                )
