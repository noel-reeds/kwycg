from flask import Flask
import os
from flask_login import LoginManager


def setup():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)
    app.url_map.strict_slashes = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trace_pesa.db'
    from models import db_engine
    db_engine.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view ='auth.login'
    login_manager.init_app(app)

    from models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

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
