from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy import create_engine
import os, app

Base = declarative_base()

engine = create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))

from .user import User
from .expense import Expense

Base.metadata.create_all(engine)
session_f = sessionmaker(bind=engine)
session = scoped_session(session_f)
Base.query = session.query_property()
