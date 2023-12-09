from datetime import timedelta
import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_smorest import Api
from wbapp.db_sqlalchemy import db

from wbapp.routes.auth import blp as UserBlueprint


def create_app():
    app = Flask(__name__)
    load_dotenv()
    url = os.getenv("DATABASE_URL")
    secret_key = os.getenv("SECRET_KEY")
    jwt_secret_key = os.getenv("SECRET_KEY")

    # Configure App
    app.config['SQLALCHEMY_DATABASE_URI'] = url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY']=secret_key

    # Configure JWT
    # app.config['JWT_SECRET_KEY']='240772518621864039464587153032836458536'
    app.config['JWT_SECRET_KEY']=jwt_secret_key
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=180)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=120)

    # SWAGGER UI
    app.config['API_TITLE']='cdms'
    app.config['API_VERSION']='v1'
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Initialize libraries with app
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)
    api = Api(app)
    jwt = JWTManager(app)

    # Register Blueprints
    api.register_blueprint(UserBlueprint, url_prefix='/api')

    # return the app
    return app

