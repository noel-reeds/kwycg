from dotenv import load_dotenv
from flask import Flask, g
import os

load_dotenv()

def setup():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.url_map.strict_slashes = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    from models import db_engine
    db_engine.init_app(app)

    from api.v1.auth.auth import auth as auth_blueprint
    from api.v1.expenses import expense as expense_blueprint
    from api.v1.users import user as users_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/api/v1')
    app.register_blueprint(expense_blueprint, url_prefix='/api/v1')
    app.register_blueprint(users_blueprint, url_prefix='/api/v1')

    return app


app = setup()

if __name__ == "__main__":
	app.run(port=8000, debug=True)
