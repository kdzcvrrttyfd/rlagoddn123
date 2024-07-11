import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv
from sqlalchemy import inspect
from sqlalchemy.exc import OperationalError
import time
load_dotenv()  # .env 파일 로드

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.routes import main, users
    app.register_blueprint(main)
    app.register_blueprint(users)


    with app.app_context():
        retries = 5
        while retries > 0:
            try:
                inspector = inspect(db.engine)
                if not inspector.has_table('user') or not inspector.has_table('item'):
                    db.create_all()
                break
            except OperationalError as e:
                retries -= 1
                print(f"DB connection failed. Retrying... ({5 - retries}/5)")
                time.sleep(5)
                if retries == 0:
                    print("DB connection failed after 5 retries.")
                    raise e
    return app
