from flask import render_template
from flask_smorest import Blueprint

blp = Blueprint('CDMS','iTraining',description='Capacity Development Management System')

@blp.route('/')
def index():
    return render_template('cdms/index.html')