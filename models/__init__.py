from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy import create_engine
import os

Base = declarative_base()

from .user import User
from .expense import Expense
from app import app

engine = create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))

Base.metadata.create_all(engine)
session_f = sessionmaker(bind=engine)
session = scoped_session(session_f)
Base.query = session.query_property()
