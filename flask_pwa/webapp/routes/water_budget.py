from flask import render_template
from flask_smorest import Blueprint
import requests

blp = Blueprint("WaterBudget","water_budget",description="water budget calculations")

class WaterBudgetCalc:

    def __init__(self, demand, supply):
        self.demand = demand
        self.supply = supply

   
    def get_water_budget(payload):
        url = 'http://127.0.0.1:3000/api/demand'
        water_demand =requests.post(url, json=payload)
        url = 'http://127.0.0.1:3000/api/supply'
        water_supply =requests.post(url, json=payload)
        return {'demand':water_demand.json(), 'supply':water_supply.json()}
