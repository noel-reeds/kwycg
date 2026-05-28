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
    from models import Expense, session
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

@expense.route('/delete/<string:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    """
    Deletes an expenditure from the database if it exists,
    otherwise return an error.

    Params:
    :expenditure_id
    """
    try:
        from models import Expense, session
        expense = session.query(Expense).filter_by(id=expense_id).first()
        if not expense:
            return {'message': 'expense does not exist!'}
        session.delete(expense)
        session.commit()
        return {'message': 'OK'}
    except Exception as e:
        return {"message": "an error occured!"}

@expense.route('/expenses', methods=['GET'])
@auth.login_required
def user_expenses():
    """
    Queries the database and returns all expenses of a
    user of any.

    Params:
    user_id of the user.
    """
    from models import Expense, session
    expenses = session.query(Expense).filter_by(user_id=g.user.id).all()
    if expenses:
        return {"expenses": [k.to_dict() for k in expenses]}
    return {'message': 'no expenses for this user'}


@expense.route('/update/<string:expense_id>', methods=['UPDATE'])
@auth.login_required
def update_expense(expense_id):
    """
    Updates a user expenditure if it exists, otherwise
    return an error.

    Params:
    :expense_id
    """
    from models import Expense, session
    try:
        if not request.is_json:
            raise Exception
        update_info = request.get_json()
        session.query(Expense).filter_by(id=expense_id).update(update_info)
        session.commit()
        return {"message": "OK"}
    except Exception as e:
        return {'message': 'An error occured!'}

@expense.route('/expense/<string:expense_id>', methods=['GET'])
@auth.login_required
def expenditure(expense_id):
    """
    Return a specific expenditure
    """
    from models import Expense, session
    try:
        e = session.query(Expense).filter_by(id=expense_id).first()
        print(e)
        if e is None:
            return {'error': 'expense does not exist!'}
        return {"expense": e.to_dict()}
    except Exception as err:
        return {"error": "{}".format(err)}
