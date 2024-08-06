from flask import Blueprint, json, redirect, render_template, request, session, url_for

from iWork.app.models import State,  District, Block, Panchayat
from iWork.app.models.works import Work
from iWork.app.models.assets_data import AssetData
from iWork.app.models.categories import Category
from iWork.app.models.input_parameters import InputParameter
from iWork.app.models.input_proposed_status import InputProposedStatus
from iWork.app.models.proposed_status import ProposedStatus


blp = Blueprint("routes", "routes")

@blp.route("/profile", methods=['POST','GET'])
def profile():
    states = Work.get_states()
    if request.method == 'POST':
        state_id = request.form.get('selectState')
        district_id = request.form.get('selectDistrict')
        block_id = request.form.get('selectBlock')
        panchayat_id = request.form.get('selectPanchayat')
        payload = {'panchayat_id': panchayat_id}        
        session['payload'] = payload
        return redirect(url_for('.data'))
    else:
        return render_template('profile.html', states = states)

@blp.route("/districts", methods=['POST'])
def get_districts():
    json_data = request.json
    if json_data is not None:
        state_id = int(json_data['select_id'])
        state_districts = Work.get_districts_by_state_id(state_id)
        # districts_dict = [district.json() for district in state_districts]
        # json_data = json.dumps(districts_dict)
    return state_districts

@blp.route("/blocks", methods=['POST'])
def get_blocks():
    json_data = request.json
    if json_data is not None:
        district_id = json_data['select_id']
        district_blocks = Work.get_blocks_by_district_id(district_id)
        # blocks_dict = [block.json() for block in district_blocks]
        # json_data = json.dumps(blocks_dict)
    return district_blocks

@blp.route("/panchayats", methods=['POST'])
def get_panchayats():
    json_data = request.json
    if json_data is not None:
        block_id = json_data['select_id']
        block_panchayats = Work.get_panchayats_by_block_id(block_id)
        # panchayats_dict = [panchayat.json() for panchayat in block_panchayats]
        # json_data = json.dumps(panchayats_dict)
    return block_panchayats

@blp.route("/data", methods=['POST','GET'])
def data():
    if session['payload']:
        payload = session['payload']
        breadcrumbs_value = Panchayat.get_panchayat_block_district_state(payload['panchayat_id'])
        breadcrumbs = [
            {'id':breadcrumbs_value['state_id'],'name':breadcrumbs_value['state_name'].title()},
            {'id':breadcrumbs_value['district_id'],'name':breadcrumbs_value['district_name'].title()},
            {'id':breadcrumbs_value['block_id'],'name':breadcrumbs_value['block_name'].title()},
            {'id':breadcrumbs_value['panchayat_id'],'name':breadcrumbs_value['panchayat_name'].title()}
        ]
    else:
        return redirect(url_for('.profile'))
    panchayat_id = payload['panchayat_id']
    if request.method == 'POST':
        asset_id = request.form.get('selectAssetID')
        category_id = request.form.get('categories')
        proposed_status_id = request.form.get('selectProposedStatus')
        asset_datalist = []
        for key, value in request.form.items():
            if key.startswith('input'):
                if value:
                    asset_data ={'asset_id':asset_id,
                                 'proposed_status_id':proposed_status_id, 
                                 'input_id':int(key[len("input"):]), 
                                 'input_value':value,
                                 'panchayat_id':panchayat_id}
                    asset_datalist.append(asset_data)
        for asset in asset_datalist:
            new_asset_data = AssetData(
                input_value=asset['input_value'],
                asset_id=asset['asset_id'],
                proposed_status_id=asset['proposed_status_id'],
                input_id=asset['input_id'],
                panchayat_id = asset['panchayat_id']
            )
            AssetData.save_to_db(new_asset_data)
        return redirect(url_for('.data'))
    else:
        assets = Work.get_assets_by_panchayat_id(panchayat_id)
        if len(assets)==0:
            return redirect(url_for('.view_assets'))
        assets_data = AssetData.get_assets_by_panchayat(panchayat_id)
        if assets_data==None:
            completed = 0
        else:
            completed = len(assets_data)
        categories = Category.get_categories_by_id()
        permissible_works = ProposedStatus.get_proposed_status_by_category()    
        return render_template('data.html', 
                           breadcrumbs=breadcrumbs, 
                           assets=assets, 
                           permissible_works = permissible_works,
                           categories=categories,
                           completed=completed)

@blp.route('/view_assets')
def view_assets():
    if session['payload']:
        payload = session['payload']
    else:
        return redirect(url_for('.profile'))    
    panchayat_id = payload['panchayat_id']
    breadcrumbs_value = Panchayat.get_panchayat_block_district_state(panchayat_id)
    breadcrumbs = [
        {'id':breadcrumbs_value['state_id'],'name':breadcrumbs_value['state_name'].title()},
        {'id':breadcrumbs_value['district_id'],'name':breadcrumbs_value['district_name'].title()},
        {'id':breadcrumbs_value['block_id'],'name':breadcrumbs_value['block_name'].title()},
        {'id':breadcrumbs_value['panchayat_id'],'name':breadcrumbs_value['panchayat_name'].title()}
    ]
    assets_data = AssetData.get_asset_data_by_panchayat(panchayat_id)
    return render_template('view_assets.html', assets_data=assets_data, breadcrumbs=breadcrumbs)

@blp.route('/update_asset/<int:id>')
def update_asset(id):
    if session['payload']:
        payload = session['payload']
        breadcrumbs_value = Panchayat.get_panchayat_block_district_state(payload['panchayat_id'])
        breadcrumbs = [
            {'id':breadcrumbs_value['state_id'],'name':breadcrumbs_value['state_name'].title()},
            {'id':breadcrumbs_value['district_id'],'name':breadcrumbs_value['district_name'].title()},
            {'id':breadcrumbs_value['block_id'],'name':breadcrumbs_value['block_name'].title()},
            {'id':breadcrumbs_value['panchayat_id'],'name':breadcrumbs_value['panchayat_name'].title()}
        ]
    else:
        return redirect(url_for('.profile'))
    assets_data = AssetData.get_asset_data_by_id(id)
    return render_template('update_asset.html', breadcrumbs=breadcrumbs)

@blp.route("/proposed_status", methods=["POST"])
def proposed_status_by_category():
    json_data = request.json
    permissible_works = ProposedStatus.get_proposed_status_by_category(category_id=json_data['select_id'])
    return permissible_works

@blp.route("/input_parameters", methods=["POST"])
def input_parameters():
    json_data = request.json
    input_parameters = InputProposedStatus.get_parameters_by_proposed_status_id(proposed_status_id=json_data['select_id'])
    return input_parameters

@blp.route("/success")
def success_page():
    return render_template('success.html')

@blp.route("/splash_screen")
def splash_screen():
    return render_template('splash_screen.html')

@blp.route("/assets", methods=['POST'])
def assets():
    json_data = request.json
    nrega_assets_id = json_data['select_id']
    asset = Work.get_assets_by_id(nrega_assets_id)
    return asset