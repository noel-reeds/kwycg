#!/usr/bin/env python3

from models import db
from app import setup
from models import Expense

app = setup()

with app.app_context():
    db.create_all()

    print("All tables created!")
