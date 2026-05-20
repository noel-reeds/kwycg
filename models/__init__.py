from flask_sqlalchemy import SQLAlchemy

db_engine = SQLAlchemy()
session = db_engine.session

from .user import User
from .expense import Expense
