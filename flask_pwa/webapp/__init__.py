from dotenv import load_dotenv
from flask import Flask
from flask_smorest import Api
from webapp.routes.pwa import blp as PwaBlueprint


def create_app():
    app = Flask(__name__)
    load_dotenv()

     # SWAGGER UI
    app.config['API_TITLE']='cdms'
    app.config['API_VERSION']='v1'
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    api = Api(app)

    # app.register_blueprint(WaterBudgetBlueprint, url_prefix='/get')
    api.register_blueprint(PwaBlueprint)

    return app