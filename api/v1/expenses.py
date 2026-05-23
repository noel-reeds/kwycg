from flask import Flask, Blueprint, request, jsonify, g
from flask import jsonify as js
from models import Expense, User
from models import session
from datetime import datetime, date
from api.v1.users import auth

expense = Blueprint('expense', __name__)

@expense.route('/add/<int:user_id>', methods=['POST'])
@auth.login_required
def add_expense(user_id):
    """
    Adds an expenditure linked to a specific user 
    to the database.

    Params:
    user_id foreign key from user table.
    """
    try:
        if not request.is_json:
            raise Exception
        r = request.json
        category = r.get('category')
        description = r.get('description')
        name = r.get('name')
        amount_spent = r.get('amount')

        new = Expense(user_id=g.user.id,
                        category=category,
                        description=description,
                        name=name,
                        amount=amount_spent
                    )
        session.add(new)
        session.commit()
        return {'message': 'OK'}
    except Exception as e:
        return {'message': 'error adding an expenditure'}

@expense.route('/delete/<uuid:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    """Deletes an expense from database"""
    expense = Expense.query.filter_by(id=expense_id).first()
    #check if expense exists
    if expense:
        db.session.delete(expense)
        db.session.commit()
        return jsonify({'message': 'expense delete success'})
    return jsonify({'message': 'expense does not exist'})

@expense.route('/expenses/<int:user_id>', methods=['GET'])
def user_expenses(user_id):
    """Returns all expenses of a user"""
    if not User.query.filter_by(id=user_id).first():
        return jsonify({'message': 'user does not exist'})
    expenses = Expense.query.filter_by(user_id=user_id).all()
    if expenses:
        # uri method drops id attr and adds URI
        return js({"expenses": [uri_for(expense.to_dict()) for expense in expenses]})
    return jsonify({'message': 'no expenses for this period'})


@expense.route('/update/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    """Updates a user expenditure"""
    expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first()
    try:
        expense_info = request.get_json()
        expense.amount = expense_info.get('amount')
        expense.name = expense_info.get('name')
        expense.desc = expense_info.get('desc')
        expense.date = date.today()

        db.session.commit()
    except:
        return jsonify({'message': 'Error occured updating expenditure'})


@expense.route('/expense/<expense_id>', methods=['GET'])
def ret_expense(expense_id):
    """Return a specific expenditure"""
    expense = Expense.query.filter_by(id=expense_id).first()
    if expense is None:
        return jsonify({"message": "expenditure does not exists"})
    try:
        return jsonify({"expense": expense.to_dict()})
    except Exception as err:
        return jsonify({"error": "{}".format(err)})
