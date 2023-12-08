import os
from dotenv import load_dotenv
from flask import Flask


def create_app():
    app = Flask(__name__)
    load_dotenv()
    url = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_DATABASE_URI'] = url
    return app