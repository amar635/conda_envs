from datetime import timedelta
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from iWater.app.db import db
from iWater.app.routes.auth import blp as UserBlueprint
from iWater.app.routes.controllers import blp as controllerBlueprint
from iWater.app.routes.pwa import blp as pwaBlueprint



def create_app():
    app = Flask(__name__)
    load_dotenv()

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DUMMY_DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY']=os.getenv("SECRET_KEY")
    app.config['JWT_SECRET_KEY']=os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=180)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=120)

    # SWAGGER UI
    app.config['API_TITLE']='iWater'
    app.config['API_VERSION']='v1'
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)
    api = Api(app)
    jwt = JWTManager(app)

    # register blueprints
     # Register Blueprints
    api.register_blueprint(UserBlueprint, url_prefix='/api')
    api.register_blueprint(pwaBlueprint, url_prefix='/pwa')
    api.register_blueprint(controllerBlueprint)


    return app