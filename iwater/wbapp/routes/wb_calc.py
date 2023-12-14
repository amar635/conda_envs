from flask import jsonify, request
from flask_smorest import Blueprint
from wbapp.classes.water_demand import WaterDemand

from wbapp.classes.available_runoff import AvailableRunoff

blp = Blueprint("Rainfall_data", "rainfall_calc", description="User Authentication")

# blp = Blueprint("Rainfall_data", "rainfall", description="rainfall related calculation")

@blp.route('/yield', methods=['POST'])
def post():
    json_data = request.json
    runoff_yield = AvailableRunoff.get_runoff_yield(rainfall=json_data['rainfall'])
    return runoff_yield

@blp.route('/demand', methods=['POST'])
def post():
    json_data = request.json
    human_demand = WaterDemand.human_consumption(json_data['village_id'])
    agriculture_demand = WaterDemand.agricuture_consumption(json_data['village_id'])
    livestock_consumption = WaterDemand.livestock_consumption(json_data['village_id'])
    return livestock_consumption


