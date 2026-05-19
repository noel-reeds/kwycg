#!/usr/bin/env python3

from models import db
from app import fintrack_app
from models import Expense

app = fintrack_app()

with app.app_context():
    db.create_all()

    print("All tables created!")
