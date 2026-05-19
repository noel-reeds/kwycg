from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session

database = SQLAlchemy()
session = Session(database)

from .user import User
from .expense import Expense
