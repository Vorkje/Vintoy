from flask import Flask
from .views import main
from .models import db
from flask_login import LoginManager

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auction.db'
    db.init_app(app)
    login_manager.init_app(app)
    app.register_blueprint(main)
    return app