from flask import Blueprint, json, redirect, render_template, request, session, url_for

from iWork.app.models import InputAndPermissible, PermissibleWork, InputParameter, Category, CompletedWork, Panchayat, FieldData
from iWork.app.models.work_types import WorkType


blp = Blueprint("routes", "routes")

@blp.route("/profile", methods=['POST','GET'])
def profile():
    states = CompletedWork.get_states()
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
        state_districts = CompletedWork.get_districts_by_state_id(state_id)
    return state_districts

@blp.route("/blocks", methods=['POST'])
def get_blocks():
    json_data = request.json
    if json_data is not None:
        district_id = json_data['select_id']
        district_blocks = CompletedWork.get_blocks_by_district_id(district_id)
    return district_blocks

@blp.route("/panchayats", methods=['POST'])
def get_panchayats():
    json_data = request.json
    if json_data is not None:
        block_id = json_data['select_id']
        block_panchayats = CompletedWork.get_panchayats_by_block_id(block_id)
    return block_panchayats

@blp.route("/data", methods=['POST','GET'])
def data():
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
    if request.method == 'POST':
        completed_work_id = request.form.get('selectWorkCode')
        permissible_work_id = request.form.get('selectPermissibleWork')
        for key, value in request.form.items():
            if key.lower().startswith('input'):
                if value:
                    field_data = FieldData(input_value=value, completed_work_id=completed_work_id, 
                       permissible_work_id=permissible_work_id, input_id=int(key[len("input"):]), 
                       panchayat_id=panchayat_id)
                    field_data.save_to_db()
        return redirect(url_for('.data'))
    else:
        categories = Category.get_categories_by_id()
        completed_works = CompletedWork.get_works_by_panchayat_id(panchayat_id)
        if len(completed_works)==0:
            return redirect(url_for('.view_assets'))
        field_data = FieldData.get_completed_work_id_by_panchayat(panchayat_id)
        if field_data:
            completed = len(field_data)
        else:
            completed = 0
        # permissible_works = PermissibleWork.get_proposed_status_by_category()    
        return render_template('data.html', 
                        breadcrumbs=breadcrumbs, 
                        completed_works=completed_works, 
                        completed=completed,
                        categories=categories)

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
    field_data = FieldData.get_field_data_by_panchayat(panchayat_id)
    return render_template('view_assets.html', breadcrumbs=breadcrumbs, field_data=field_data)

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
    # assets_data = AssetData.get_asset_data_by_id(id)
    return render_template('update_asset.html', breadcrumbs=breadcrumbs)

@blp.route("/permissible_works", methods=["POST"])
def permissible_work_by_category():
    json_data = request.json
    permissible_works = PermissibleWork.get_permissible_work_by_work_type(json_data['select_id'])
    return permissible_works

@blp.route("/work_types", methods=["POST"])
def work_types_by_category():
    json_data = request.json
    work_types = WorkType.get_work_types_by_category(json_data['select_id'])
    return work_types

@blp.route("/input_parameters", methods=["POST"])
def input_parameters():
    json_data = request.json
    input_parameters = InputAndPermissible.get_parameters_by_permissible_work_id(permissible_work_id=json_data['select_id'])
    return input_parameters

@blp.route("/success")
def success_page():
    return render_template('success.html')

@blp.route("/")
def splash_screen():
    return render_template('splash_screen.html')

@blp.route("/assets", methods=['POST'])
def assets():
    json_data = request.json
    nrega_assets_id = json_data['select_id']
    asset = CompletedWork.get_assets_by_id(nrega_assets_id)
    return asset