#!/usr/bin/env python3

from models import db_engine
from app import setup
from models import Expense, User

app = setup()

with app.app_context():
    db_engine.create_all()

    print("All tables created!")
