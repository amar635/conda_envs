from dotenv import load_dotenv
from flask import Flask
from flask import Flask, redirect, url_for
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from iCore.app.models.user import User
from iCore.app.db import db
from iCore.app.routes.auth import blp as authBlueprint
from iCore.app.routes.routes import blp as routesBlueprint


def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

    # db.init_app(app)
    login_manager = LoginManager(app)
    jwt = JWTManager(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    app.register_blueprint(authBlueprint)
    app.register_blueprint(routesBlueprint)

    return app