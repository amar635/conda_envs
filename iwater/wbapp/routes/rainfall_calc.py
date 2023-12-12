from flask import request
from flask_smorest import Blueprint

from wbapp.classes.available_runoff import AvailableRunoff

blp = Blueprint("Rainfall_data", "rainfall_calc", description="User Authentication")

# blp = Blueprint("Rainfall_data", "rainfall", description="rainfall related calculation")

@blp.route('/yield', methods=['POST'])
def post():
    json_data = request.json
    runoff_yield = AvailableRunoff.get_runoff_yield(json_data['rainfall'], json_data['catchment_type'])
    return {"Runoff Yield": str(runoff_yield)}


