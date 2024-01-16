from datetime import timedelta
import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from flask_migrate import Migrate
from flask_cors import CORS
from cdmsapp.extensions import db
from cdmsapp.models import TokenBlocklistModel

from cdmsapp.routes.user import blp as UserBlueprint
from cdmsapp.routes.event import blp as EventBlueprint
from cdmsapp.routes.particpant import blp as ParticipantBlueprint
from cdmsapp.routes.external_api import blp as ExternalApiBlueprint
from cdmsapp.routes.pdf_to_audio import blp as HtmlApiBlueprint
from cdmsapp.routes.project_financials import blp as DashboardBlueprint
from cdmsapp.routes.strange import blp as StrangeBlueprint

def create_app(db_url=None):
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
    app.config['SECRET_KEY']='b5e4e6b5b74e9fc20b477ebe62bed84188daf2a581a793d61c2c61ac7cee68a0'
    app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif','.pdf','pdf']
    app.config['UPLOAD_FOLDER'] =os.path.join(os.getcwd(),'cdmsapp/static/uploads')
    # app.config['UPLOAD_PATH'] = os.path.join(os.getcwd(),app.config['UPLOAD_PATH'])
    app.config['API_TITLE']='pwa'
    app.config['API_VERSION']='v1'
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config['SQLALCHEMY_DATABASE_URI']= "postgresql://vzaqkttf:o_UOxLNY6_gjA-sgu-iLGgFOElOVgNLI@john.db.elephantsql.com/vzaqkttf"
    # app.config['SQLALCHEMY_DATABASE_URI']=db_url or os.getenv('DATABASE_URL', "sqlite:///db.sqlite")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS']=True


    api = Api(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)
    # cors = CORS(app, origins='*', resources='*')

    app.config['JWT_SECRET_KEY']='240772518621864039464587153032836458536'
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=180)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=120)
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload["jti"]
        token = TokenBlocklistModel.find_by_jti(jti)
        # db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

        return token is not None

    #IMPORTANT - required for sqlite to create all tables
    #To be commented out when using postgres
    # @app.before_first_request
    # def create_tables():
    #     db.create_all()


    api.register_blueprint(UserBlueprint)
    api.register_blueprint(EventBlueprint)
    api.register_blueprint(ParticipantBlueprint)
    api.register_blueprint(ExternalApiBlueprint)
    api.register_blueprint(HtmlApiBlueprint)
    api.register_blueprint(DashboardBlueprint)
    api.register_blueprint(StrangeBlueprint)

    return app


