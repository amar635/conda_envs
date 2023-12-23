from flask import make_response, render_template, request, send_from_directory
from flask_smorest import Blueprint
import requests

from webapp.routes.water_budget import WaterBudgetCalc

blp = Blueprint("PWA", "pwa_calls", description="api call for pwa")

# blp = Blueprint("Rainfall_data", "rainfall", description="rainfall related calculation")

@blp.route('/index', methods=['POST'])
def index():
    # calculate demand
    state_id = request.form.get('ddStates')
    district_id = request.form.get('ddDistricts')
    block_id = request.form.get('ddBlocks')
    village_id = request.form.get('ddVillages')
    payload = {'village_id': village_id}
    if (village_id == -1 or village_id is None):
        payload = {'block_id': block_id}
    if (block_id == -1 or block_id is None):
        payload = {'district_id': district_id}
    agriculture_demand, human_demand, livestock_demand = 0, 0, 0
    wb = WaterBudgetCalc.get_water_budget(payload=payload)
    demand = wb['demand']
    agriculture = demand['agriculture']
    for item in range(len(agriculture)):
        agriculture_demand = agriculture[item]['demand'] + agriculture_demand
    human = demand['human']
    for item in range(len(human)):
        human_demand = human[item]['demand'] + human_demand
    livestock = demand['livestock']
    for item in range(len(livestock)):
        livestock_demand = livestock[item]['demand'] + livestock_demand
    # calculate supply
    available_runoff, harvested_runoff = 0, 0
    supply = wb['supply']
    available = supply['available']
    available_runoff = available['good'] + available['average'] + available['bad']
    harvested= supply['harvested']
    for item in range(len(harvested)):
        harvested_runoff = harvested[item]['area'] + harvested_runoff  
    # calculate water budget
    water_demand = agriculture_demand + human_demand + livestock_demand
    water_supply = available_runoff + harvested_runoff
    return render_template('pwa/index.html',
                           water_demand_labels = ["Human", "Agriculture", "Livestock"],
                           water_demand = [round(human_demand,1),round(agriculture_demand,1),round(livestock_demand,1)],
                           water_supply_labels = ["harvested", "available"],
                           water_supply = [round(harvested_runoff,2), round(available_runoff,2)],
                           water_budget_labels = ['demand','supply'],
                           water_budget_data = [round(water_demand,2), round(water_supply,2)])

# def index():
#     wb = WaterBudgetCalc.get_water_budget()
#     agriculture = wb['agriculture']
#     human = wb['human']
#     livestock = wb['livestock']
#     return render_template('pwa/index.html',
#                            water_demand_labels = ['human', 'agriculture', 'livestock'],
#                            water_demand = [agriculture['demand'],human['demand'],livestock['demand']]
                        #    )

@blp.route("/error")
def fallback():
    return render_template('pwa/fallback.html')
    

@blp.route('/sw.js')
def service_worker():
    response = make_response(send_from_directory('static', 'sw.js'))
    response.headers['Cache-Control'] = 'no-cache'
    return response

@blp.route('/about')
def about():
    # wb = WaterBudgetCalc.get_water_budget()
    return render_template('pwa/about.html')

@blp.route('/select')
def select_state():
    url = 'http://127.0.0.1:3000/api/states'
    states = requests.post(url)
    return render_template('pwa/dropdown.html', states = states.json())

@blp.route('/districts',methods=['POST'])
def select_state():
    json_data = request.json
    url = 'http://127.0.0.1:3000/api/districts'
    districts = requests.post(url, json=json_data)
    return districts.json()

@blp.route('/blocks',methods=['POST'])
def select_state():
    json_data = request.json
    url = 'http://127.0.0.1:3000/api/blocks'
    blocks = requests.post(url, json=json_data)
    return blocks.json()

@blp.route('/villages',methods=['POST'])
def select_state():
    json_data = request.json
    url = 'http://127.0.0.1:3000/api/villages'
    villages = requests.post(url, json=json_data)
    return villages.json()

# @blp.route('/submit',methods=['POST'])
# def select_state():
#     json_data = request.json
#     url = 'http://127.0.0.1:3000/api/villages'
#     villages = requests.post(url, json=json_data)
#     return villages.json()