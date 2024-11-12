from flask import Blueprint, json, make_response, redirect, render_template, request, session, url_for

from iJalagam.app.models import Block, District, State 
from iJalagam.app.models.water_budget import WaterBudget
# from app.models.census_data import CensusData
# from app.models.districts import District
# from app.models.groundwater_extraction import GroundwaterExtraction
# from app.models.rainfall import RainfallDatum
# from app.models.states import State
# from app.models.strange_table import StrangeRunoff
# from app.models.water_budget import WaterBudget
# from app.models.waterbody_census import WaterbodyCensus


blp = Blueprint('routes', 'routes')

@blp.route('/index', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        state_id = request.form.get('selectState')
        district_id = request.form.get('selectDistrict')
        block_id = request.form.get('selectBlock')
        if block_id:
            payload = WaterBudget.get_session_payload(block_id, district_id, state_id)
        if session is not None:
            session['payload'] = ''
        session['payload'] = payload
        return redirect(url_for('.home'))
    states = State.get_states()
    return render_template('select_panchayat.html', states=states)

@blp.route("/districts", methods=['POST'])
def districts():
    json_data = request.json
    if json_data is not None:
        state_id = int(json_data['state_id'])
    else:
        return make_response('', 400)
    districts = District.get_districts(state_id)
    if districts:
        return districts
    else:
        return make_response('', 400)

@blp.route("/blocks", methods=['POST'])
def blocks():
    json_data = request.json
    if json_data is not None:
        district_id = int(json_data['district_id'])
    else:
        return make_response('', 400)
    blocks = Block.get_blocks(district_id)
    if blocks:
        return blocks
    else:
        return make_response('', 400)

# DEMAND SIDE
@blp.route('/human')
def human():
    if session:
        payload = session['payload']
    else:
        redirect(url_for('routes.index'))
    district = payload['district']
    block = payload['block']
    human, chart_data = WaterBudget.get_human_demand(block_id=block['id'], district_id=district['id'])
    breadcrumbs = get_breadcrumbs(payload)
    return render_template('demand/human.html', human=human, chart_data = json.dumps(chart_data), breadcrumbs=breadcrumbs)



@blp.route('/livestock')
def livestock():
    if session:
        payload = session['payload']
    else:
        redirect(url_for('routes.index'))
    district = payload['district']
    block = payload['block']
    livestocks, chart_data = WaterBudget.get_livestock_demand(block_id=block['id'], district_id=district['id'])
    breadcrumbs = get_breadcrumbs(payload)
    return render_template('demand/livestock.html', livestocks = livestocks, 
                           breadcrumbs = breadcrumbs, chart_data = json.dumps(chart_data))

@blp.route('/crops')
def crops():
    if session:
        payload = session['payload']
    else:
        redirect(url_for('routes.index'))
    district = payload['district']
    block = payload['block']
    crop_data, chart_data = WaterBudget.get_crops_demand(block['id'], district['id'])
    breadcrumbs = get_breadcrumbs(payload)
    # sorted_json_array = sorted(json_array, key=lambda x: (x['crop_area']), reverse=True)
    return render_template('demand/crop.html', crops = crop_data, 
                           chart_data = json.dumps(chart_data), 
                           breadcrumbs=breadcrumbs)

@blp.route('/industry')
def industry():
    return render_template('demand/industry.html')

# SUPPLY SIDE

@blp.route('/rainfall')
def rainfall():
    if session:
        payload = session['payload']
    else:
        redirect(url_for('routes.index'))
    district = payload['district']
    block = payload['block']
    rainfall, monthwise_rainfall, chart_data = WaterBudget.get_rainfall(block['id'], district['id'])
    breadcrumbs = get_breadcrumbs(payload)
    return render_template('supply/rainfall.html', 
                           rainfalls=rainfall, breadcrumbs=breadcrumbs, monthwise_rainfall=monthwise_rainfall,
                           chart_data=json.dumps(chart_data))

@blp.route('/surface')
def surface():
    if session:
        payload = session['payload']
    else:
        return redirect(url_for('routes.index'))
    district = payload['district']
    block = payload['block']
    waterbodies, sorted_waterbodies, chart_data = WaterBudget.get_surface_supply(block['id'],district['id'])
    breadcrumbs = get_breadcrumbs(payload=payload)   
    return render_template('supply/harvested.html', waterbodies = waterbodies, 
                           sorted_waterbodies=sorted_waterbodies,
                           breadcrumbs = breadcrumbs, chart_data = json.dumps(chart_data))

@blp.route('/ground')
def ground():
    if session:
        payload = session['payload']
    else:
        redirect(url_for('routes.index'))
    district = payload['district']
    block = payload['block']
    gw_data, chart_data = WaterBudget.get_ground_supply(block_id=block['id'], district_id=district['id'])
    print(chart_data)
    breadcrumbs = get_breadcrumbs(payload=payload)
    return render_template('supply/groundwater.html', chart_data=json.dumps(chart_data), 
                           gw_data=gw_data, table_data=chart_data,  breadcrumbs=breadcrumbs)

@blp.route('/runoff')
def runoff():
    if session:
        payload = session['payload']
    else:
        redirect(url_for('routes.index'))
    district = payload['district']
    block = payload['block']
    runoffs, catchments, chart_data = WaterBudget.get_runoff(block['id'], district['id'])
    breadcrumbs = get_breadcrumbs(payload)
    return render_template('supply/runoff.html', runoffs=runoffs, catchments=catchments, 
                           breadcrumbs=breadcrumbs, chart_data = json.dumps(chart_data))

@blp.route('/home')
def home():
    if session:
        payload = session['payload']
    else:
        redirect(url_for('routes.index'))
    district = payload['district']
    block = payload['block']
    demand, demand_chart_data = WaterBudget.get_total_demand(block['id'], district['id'])  
    supply, supply_chart_data = WaterBudget.get_total_supply(block['id'], district['id'])  
    water_budget = [{'name':'Demand','consumption':demand, 'background':'success'},
                    {'name':'Supply','consumption':supply, 'background':'danger'}]
    # total = demand + supply
    chart_data = {'demand':demand_chart_data, 'supply':supply_chart_data}
    return render_template('budget.html', 
                           water_budget = water_budget, 
                           chart_data = json.dumps(chart_data),
                           breadcrumbs = get_breadcrumbs(payload))

@blp.route('/external')
def external():
    return render_template('supply/external.html')

def get_breadcrumbs(payload):
    state = payload['state']
    district = payload['district']
    block = payload['block']
    breadcrumbs = [
        {'name': state['name'], 'href': '/'},
        {'name': district['name'], 'href': '/'},
        {'name': block['name'], 'href': '/'},
        ]
        
    return breadcrumbs

## LINKS
# DEMAND
# Livestock - https://dahd.nic.in/schemes/programmes/animal-husbandry-statistics
# Crops - https://data.desagri.gov.in/website/crops-apy-report-web
# Census Data - /Users/amar/Library/CloudStorage/OneDrive-DeutscheGesellschaftfürInternationaleZusammenarbeit(GIZ)GmbH/WASCA II/Niti Aayog

# SUPPLY
# Rainfall - https://indiawris.gov.in/wris/#/rainfall
# Groundwater - https://ingres.iith.ac.in/api/gec/getBusinessDataForUserOpen
# Waterbody Data - /Users/amar/Library/CloudStorage/OneDrive-DeutscheGesellschaftfürInternationaleZusammenarbeit(GIZ)GmbH/WASCA II/Niti Aayog
