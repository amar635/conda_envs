from flask import Blueprint, flash, g, get_flashed_messages, json, make_response, redirect, render_template, request, session, url_for
from flask_login import login_required, current_user
from datetime import datetime
from iWork.app.models import InputAndPermissible, PermissibleWork, InputParameter, Category, CompletedWork, Panchayat, FieldData, State, WorkType, User


blp = Blueprint("routes", "routes")

"""
Handles HTTP requests to the '/profile' route.

This function is responsible for retrieving a list of states and rendering the 'profile.html' template.
If the request method is 'POST', it retrieves the selected state, district, block, and panchayat IDs from the request form,
stores the panchayat ID in the session payload, and redirects the user to the '/data' route.

Parameters:
    None

Returns:
    A rendered 'profile.html' template or a redirect response to the '/data' route.
"""

@blp.route("/profile", methods=['POST','GET'])
@login_required
def profile():
    message = 'false'
    messages = get_flashed_messages(with_categories=True)
    if messages:
        if messages[0][0] == 'error':
            message = messages[0][1]
    states = State.get_states()
    selected_state = current_user.state_id
    state_districts = CompletedWork.get_districts_by_state_id(selected_state)
    if request.method == 'POST':
        # state_id = request.form.get('selectState')
        # district_id = request.form.get('selectDistrict')
        # block_id = request.form.get('selectBlock')
        panchayat_id = request.form.get('selectPanchayat')
        payload = {'panchayat_id': panchayat_id}        
        session['payload'] = payload
        return redirect(url_for('.data'))
    else:
        return render_template('profile.html', states = states, 
                               selected_state = selected_state, 
                               state_districts = state_districts,
                               flash_message = message)

@blp.route("/districts", methods=['POST'])
@login_required
def get_districts():
    json_data = request.json
    if json_data is not None:
        state_id = int(json_data['select_id'])
        state_districts = CompletedWork.get_districts_by_state_id(state_id)
    return state_districts

@blp.route("/blocks", methods=['POST'])
@login_required
def get_blocks():
    json_data = request.json
    if json_data is not None:
        district_id = json_data['select_id']
        district_blocks = CompletedWork.get_blocks_by_district_id(district_id)
    return district_blocks

@blp.route("/panchayats", methods=['POST'])
@login_required
def get_panchayats():
    json_data = request.json
    if json_data is not None:
        block_id = json_data['select_id']
        block_panchayats = CompletedWork.get_panchayats_by_block_id(block_id)
    return block_panchayats

@blp.route("/data", methods=['POST','GET'])
@login_required
def data():
    messages = get_flashed_messages(with_categories=True)
    message = 'false'
    if messages:
        if messages[0][0]=='success':
            message = messages[0][1]
    
    if 'payload' in session:
        payload = session['payload']
    else:
        return redirect(url_for('.profile'))
    panchayat_id = payload['panchayat_id']
    breadcrumbs = get_breadcrumbs(panchayat_id)
    if request.method == 'POST':
        session['completed_work_id'] = request.form.get('selectWorkCode')
        session['permissible_work_id'] = request.form.get('selectPermissibleWork')
        return redirect(url_for('.other_works'))
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
                        categories=categories,
                        flash_message=message)
    
@blp.route('/plantation', methods=['POST','GET'])
def plantation():
    if 'payload' in session:
        payload = session['payload']
    else:
        return redirect(url_for('.profile'))
    panchayat_id = payload['panchayat_id']
    breadcrumbs = get_breadcrumbs(panchayat_id)
    if 'completed_work_id' in session:
        completed_work_id = session['completed_work_id']
        # session.pop('completed_work_id', None)
    else:
        return redirect(url_for('.data'))
    # get permissible work id
    if 'permissible_work_id' in session:
        permissible_work_id = session['permissible_work_id']
        # session.pop('permissible_work_id', None)
    else:
        return redirect(url_for('.data'))
    if request.method == 'POST':
        permissible_work_id = request.form.get('permissible_work_id')
        completed_work_id = request.form.get('completed_work_id')
        plantation_area = request.form.get('plantation_area')
        plants_array = request.form.get('plants_array')
        plants_array = json.loads(plants_array) # convert to json array
        number_of_plants = 0
        plant_counts = ""
        plants = ""
        for plant in plants_array:
            if plant:
                number_of_plants = number_of_plants + int(plant['numbers'])
                plants = plants + plant['plant_type'] + ','
                plant_counts = plant_counts + plant['numbers'] + ","
        created_by_id = current_user.id
        created_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        input_parameters = InputAndPermissible.get_parameters_by_permissible_work_id(permissible_work_id=permissible_work_id)
        for parameter in input_parameters:
            if 'plantation area' in parameter['label'].lower():
                input_value = plantation_area
            elif 'plants number' in parameter['label'].lower():
                input_value = number_of_plants
            elif 'plant type' in parameter['label'].lower():
                input_value = plants[:-1]
            elif 'plants/trees number' in parameter['label'].lower():
                input_value = plant_counts[:-1]
            field_data = FieldData(panchayat_id=panchayat_id, 
                                   completed_work_id=completed_work_id,
                                   permissible_work_id=permissible_work_id,
                                   input_value = input_value,
                                   input_id = parameter['id'],
                                   created_by_id=created_by_id,
                                   created_on=created_on)
            field_data.save_to_db()
        completed_works = CompletedWork.get_works_by_panchayat_id(panchayat_id)
        if len(completed_works)==0:
            return render_template('success.html')
        else:
            flash('Data submitted successfully!', 'success')
            return redirect(url_for('.data'))
    completed_work_id = request.cookies.get('completed_work_id')
    permissible_work_id = request.cookies.get('permissible_work_id')
    completed_work = CompletedWork.get_completed_work_by_id(id=completed_work_id)
    input_parameters = InputAndPermissible.get_parameters_by_permissible_work_id(permissible_work_id=permissible_work_id)
    return render_template('plantation.html', input_parameters=input_parameters, completed_work=completed_work, breadcrumbs=breadcrumbs)

@blp.route('/others', methods=['POST','GET'])
def other_works():
    # get panchayat id
    if 'payload' in session:
        payload = session['payload']
    else:
        return redirect(url_for('.profile'))    
    panchayat_id = payload['panchayat_id']
    if request.method=='POST':
        completed_work_id=request.form.get('completed_work_id'),
        permissible_work_id=request.form.get('permissible_work_id')
        panchayat_id=panchayat_id
        created_by_id=current_user.id
        created_on=datetime.now().strftime("%Y-%m-%d %H:%M:%S")       
        for key, value in request.form.items():
            if key.lower().startswith('input'):
                if value:
                    field_data = FieldData(input_value=value, completed_work_id=completed_work_id, 
                       permissible_work_id=permissible_work_id, input_id=int(key[len("input"):]), 
                       panchayat_id=panchayat_id, created_by_id=created_by_id, created_on=created_on)
                    field_data.save_to_db()
        completed_works = CompletedWork.get_works_by_panchayat_id(panchayat_id)
        if len(completed_works)==0:
            return render_template('success.html')
        else:
            flash('Data submitted successfully!', 'success')
            return redirect(url_for('.data'))
    # get completed work id  
    if 'completed_work_id' in session:
        completed_work_id = session['completed_work_id']
        # session.pop('completed_work_id', None)
    else:
        return redirect(url_for('.data'))
    # get permissible work id
    if 'permissible_work_id' in session:
        permissible_work_id = session['permissible_work_id']
        # session.pop('permissible_work_id', None)
    else:
        return redirect(url_for('.data'))
    # get data from database 
    completed_work = CompletedWork.get_completed_work_by_id(id=completed_work_id)
    input_parameters = InputAndPermissible.get_parameters_by_permissible_work_id(permissible_work_id=permissible_work_id)
    for parameter in input_parameters:
        if 'list' in parameter['element_type'].lower():
            return redirect(url_for('.plantation'))
        
    return render_template('other_works.html', 
                           breadcrumbs=get_breadcrumbs(panchayat_id=panchayat_id), 
                           completed_work=completed_work, 
                           input_parameters=input_parameters)

@blp.route('/recharge_pit')
def recharge_pit():
    if 'payload' in session:
        payload = session['payload']
    else:
        return redirect(url_for('.profile'))
    panchayat_id = payload['panchayat_id']
    breadcrumbs = get_breadcrumbs(panchayat_id)
    return render_template('recharge_pit.html', breadcrumbs=breadcrumbs)

@blp.route('/field_data')
def field_data():
    field_data = FieldData.get_field_data()
    return render_template('field_data.html', field_data=field_data)

@blp.route('/all_parameters')
def all_parameters():
    input_parameters = InputParameter.get_all_parameters()
    return render_template('all_parameters.html', input_parameters=input_parameters)
@blp.route('/canal')
def canal():
    if 'payload' in session:
        payload = session['payload']
    else:
        return redirect(url_for('.profile'))
    panchayat_id = payload['panchayat_id']
    breadcrumbs = get_breadcrumbs(panchayat_id)
    return render_template('canal.html', breadcrumbs=breadcrumbs)
@blp.route('/view_assets')
@login_required
def view_assets():
    if 'payload' in session:
        payload = session['payload']
    else:
        return redirect(url_for('.profile'))    
    panchayat_id = payload['panchayat_id']
    breadcrumbs = get_breadcrumbs(panchayat_id)
    field_data = FieldData.get_field_data_by_panchayat(panchayat_id=panchayat_id)
    return render_template('view_assets.html', breadcrumbs=breadcrumbs, field_data=field_data)



@blp.route('/parameters', methods=['POST', 'GET'])
def parameters():
    if request.method=='POST':
        permissible_work_id = request.json
        input_parameters = InputAndPermissible.get_parameters_by_permissible_work_id(permissible_work_id=permissible_work_id['permissible_work_id'])
        return input_parameters
    else:
        permissible_works = PermissibleWork.get_all()
        return render_template('parameters.html', permissible_works=permissible_works)

@blp.route('/update_parameter/<int:parameter_id>', methods=['POST','GET'])
def update_parameter(parameter_id):
    input_parameter = InputParameter.get_parameter_by_id(parameter_id)
    if request.method=='POST':
        for key,value in input_parameter.items():
            if key!='id':
                input_parameter[key] = request.form.get(key)
        input_parameter['id'] = parameter_id
        result = InputParameter.update_db(input_parameter, parameter_id)
        if result:
            return redirect(url_for('.parameters'))
        else:
            return flash('There was an error')
    else:        
        return render_template('edit_parameter.html', input_parameter=input_parameter)


@blp.route('/update_asset')
@login_required
def update_asset():
    if 'payload' in session:
        payload = session['payload']
        panchayat_id = payload['panchayat_id']
        breadcrumbs = get_breadcrumbs(panchayat_id)
    else:
        flash(message='Please select panchayat', category='error')
        return redirect(url_for('.profile'))
    # assets_data = AssetData.get_asset_data_by_id(id)
    return render_template('update_asset.html', breadcrumbs=breadcrumbs)

@blp.route("/permissible_works", methods=["POST"])
@login_required
def permissible_work_by_category():
    json_data = request.json
    permissible_works = PermissibleWork.get_permissible_work_by_work_type(json_data['select_id'])
    return permissible_works

@blp.route("/work_types", methods=["POST"])
@login_required
def work_types_by_category():
    json_data = request.json
    work_types = WorkType.get_work_types_by_category(json_data['select_id'])
    return work_types

@blp.route("/input_parameters", methods=["POST"])
@login_required
def input_parameters():
    json_data = request.json
    input_parameters = InputAndPermissible.get_parameters_by_permissible_work_id(permissible_work_id=json_data['select_id'])
    return input_parameters

@blp.route("/success")
@login_required
def success():
    return render_template('success.html')

@blp.route("/")
def splash_screen():
    return render_template('splash_screen.html')

@blp.route("/assets", methods=['POST'])
@login_required
def assets():
    json_data = request.json
    nrega_assets_id = json_data['select_id']
    asset = CompletedWork.get_assets_by_id(nrega_assets_id)
    return asset 

@blp.route("/users")
def get_users():
    users = User.get_all_users()
    return render_template('users.html', users=users)

def get_breadcrumbs(panchayat_id):
    breadcrumbs_value = Panchayat.get_panchayat_block_district_state(panchayat_id)
    breadcrumbs = [
        {'id':breadcrumbs_value['state_id'],'name':breadcrumbs_value['state_name'].title()},
        {'id':breadcrumbs_value['district_id'],'name':breadcrumbs_value['district_name'].title()},
        {'id':breadcrumbs_value['block_id'],'name':breadcrumbs_value['block_name'].title()},
        {'id':breadcrumbs_value['panchayat_id'],'name':breadcrumbs_value['panchayat_name'].title()}
    ]
    return breadcrumbs