import json
from flask import jsonify, request
from flask_smorest import Blueprint
from wbapp.classes.water_demand import WaterDemand
from wbapp.models.state import State

from wbapp.models.strange_table import StrangeRunoff
from wbapp.classes.water_supply import WaterSupply

blp = Blueprint("Water_Budget", "water_budget", description="water budget calculation")

# blp = Blueprint("Rainfall_data", "rainfall", description="rainfall related calculation")

@blp.route('/yield', methods=['POST'])
def post():
    json_data = request.json
    runoff_yield = StrangeRunoff.get_runoff_yield(rainfall=json_data['rainfall'])
    return runoff_yield

@blp.route('/demand', methods=['POST'])
def post():
    json_data = request.json
    human_demand = WaterDemand.human_consumption(json_data['village_id'])
    agriculture_demand = WaterDemand.agricuture_consumption(json_data['village_id'])
    livestock_demand = WaterDemand.livestock_consumption(json_data['village_id'])
    return jsonify({ 'livestock' : livestock_demand, 'agriculture': agriculture_demand, 'human': human_demand })


@blp.route("/supply", methods=['POST'])
def post():
    json_data = request.json
    available_runoff = WaterSupply.get_available_runoff(json_data['village_id'])
    harvested_runoff = WaterSupply.get_harvested_runoff(village_id=json_data['village_id'])
    return {"available": available_runoff, "harvested": harvested_runoff}

@blp.route("/states", methods=['GET','POST'])
def get():
    states = State.get_states()
    states_json = []
    for state in states:
        states_json.append(state.json())
    return states_json



from sqlalchemy.ext.declarative import DeclarativeMeta

class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)