from flask import Blueprint, request, g
from flask import jsonify as js, jsonify
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
        from models.expense import Expense
        from models import session
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
    """
    Deletes an expenditure from the database if it exists,
    otherwise return an error.

    Params:
    :expenditure_id
    """
    try:
        from models import Expense
        from models import session
        expense = Expense.query.filter_by(id=expense_id).first()
        if not expense:
            return {'message': 'expense does not exist!'}
        session.delete(expense)
        session.commit()
        return {'message': 'OK'}
    except Exception as e:
        return {"message": "an error occured!"}

@expense.route('/expenses/<int:user_id>', methods=['GET'])
@auth.login_required
def user_expenses(user_id):
    """
    Queries the database and returns all expenses of a
    user of any.

    Params:
    user_id of the user.
    """
    from models.expense import Expense
    expenses = Expense.query.filter_by(user_id=user_id).all()
    if expenses:
        return {"expenses": [uri_for(expense.to_dict()) for k in expenses]}
    return jsonify({'message': 'no expenses for this user'})


@expense.route('/update/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    """Updates a user expenditure"""
    from models.expense import Expense
    expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first()
    try:
        expense_info = request.get_json()
        expense.amount = expense_info.get('amount')
        expense.name = expense_info.get('name')
        expense.desc = expense_info.get('desc')
        expense.date = date.today()
        from models import session
        session.commit()
    except:
        return jsonify({'message': 'Error occured updating expenditure'})


@expense.route('/expense/<expense_id>', methods=['GET'])
def ret_expense(expense_id):
    """
    Return a specific expenditure
    """
    from models.expense import Expense
    expense = Expense.query.filter_by(id=expense_id).first()
    if expense is None:
        return {"message": "expenditure does not exists"}
    try:
        return {"expense": expense.to_dict()}
    except Exception as err:
        return {"error": "{}".format(err)}
