from collections import Counter
from datetime import date
import datetime
import html
from flask import render_template, request, session
from flask_smorest import Blueprint, abort

from cdmsapp.models import projectDataModel, pywfModel, FinancialDataModel
from cdmsapp.schemas import FinancialDataSchema

blp = Blueprint("dashboard", "dashboards",
                description="html pages for financial dashboard")


@blp.route("/dashboard", methods=['GET', 'POST'])
def financials():
    # if the page is submitted capture the project or year in the sesssion
    if request.method == 'POST':
        if "filter_project" in session:
            selected_project = session["filter_project"]
        if "filter_year" in session:
            selected_year = session["filter_year"]
        # Selected project function and methods
        if "projectName" in request.form:
            selected_project = int(request.form['projectName'])
            session["filter_project"] = selected_project
        # Selected year functions and methods
        if "projectYear" in request.form:
            selected_year = int(request.form['projectYear'])
            session["filter_year"] = selected_year
    else:  # else initiate the session values
        selected_project = 1
        session["filter_project"] = selected_project
        selected_year = date.today().year
        session["filter_year"] = selected_year

    # Get all projects of NRMAe
    projects = projectDataModel.get_all_projects()
    # get specific project requirement
    project = projectDataModel.find_by_id(int(selected_project))
    # get project financials - month wise planned and actual expenses of the project
    project_financials = FinancialDataModel.find_by_project_id_and_year(
        selected_year, selected_project)

    # make the financial data table with cummulatives and gaps
    month_on_month = []
    twelve_months = get_calendar_months()
    for row in project_financials:
        monthly_expenses = {}
        for mon in twelve_months:
            if (row['month_year'].strftime('%b') == mon['short_month']):
                monthly_expenses['month_only'] = mon['short_month']
                monthly_expenses['month_year'] = row['month_year']
                monthly_expenses['planned'] = round(row['planned'], 2)
                monthly_expenses['actuals'] = round(row['actuals'], 2)
                monthly_expenses['gap'] = monthly_expenses['actuals'] - \
                    monthly_expenses['planned']
                monthly_expenses['percent'] = monthly_expenses['gap'] / \
                    monthly_expenses['planned']
                if (len(month_on_month) == 0):
                    monthly_expenses['cumm_planned'] = monthly_expenses['planned']
                    monthly_expenses['cumm_actuals'] = monthly_expenses['actuals']
                else:
                    monthly_expenses['cumm_planned'] = month_on_month[len(
                        month_on_month)-1]['cumm_planned']+monthly_expenses['planned']
                    monthly_expenses['cumm_actuals'] = month_on_month[len(
                        month_on_month)-1]['cumm_actuals'] + monthly_expenses['actuals']
                monthly_expenses['cumm_gap'] = monthly_expenses['cumm_actuals'] - \
                    monthly_expenses['cumm_planned']
                monthly_expenses['cumm_percent'] = monthly_expenses['cumm_gap'] / \
                    monthly_expenses['cumm_planned']
                break
        if monthly_expenses:
            month_on_month.append(monthly_expenses)
    # prepare mixed chart labels and dataset]
    # arrays to store data for the whole calendar year
    labels_month, planned, actuals, cumm_planned, cumm_actuals = [], [], [], [], []
    # arrays to store data till date (hence td)
    labels_td, planned_td, actuals_td, cumm_planned_td, cumm_actuals_td = [], [], [], [], []
    for idx, row in enumerate(month_on_month):
        # fill the dataset and labels for the whole calendar year
        labels_month.append(row['month_only'])
        planned.append(row['planned'])
        actuals.append(row['actuals'])
        cumm_planned.append(row['cumm_planned'])
        cumm_actuals.append(row['cumm_actuals'])
        # fill the dataset and labels array till the current month
        if idx == 0:
            labels_td.append(row['month_only'])
            planned_td.append(row['planned'])
            actuals_td.append(row['actuals'])
            cumm_planned_td.append(row['cumm_planned'])
            cumm_actuals_td.append(row['cumm_actuals'])
        elif (month_on_month[idx-1]['cumm_actuals'] < row['cumm_actuals']):
            labels_td.append(row['month_only'])
            planned_td.append(row['planned'])
            actuals_td.append(row['actuals'])
            cumm_planned_td.append(row['cumm_planned'])
            cumm_actuals_td.append(row['cumm_actuals'])
    # get project year on year data and transpose it for display
    pywf = pywfModel.find_by_projects_id(selected_project)
    year_on_year = []
    hasYoyData = False
    if len(pywf) > 0:
        column_names = pywf[0].__table__.columns.keys()
        if len(column_names) > 0:
            hasYoyData = True
            for i in range(len(column_names)):
                if(i > 2):
                    if(column_names[i] != 'projects_id'):
                        row = {}
                        row['description'] = column_names[i]
                        for j in range(len(pywf)):
                            row[str(getattr(pywf[j], 'year'))] = getattr(
                                pywf[j], column_names[i])
                        year_on_year.append(row)
    # create an array with count project['projectType'] from the list of project
    # Using the Counter class from the collections module to count the project types
    project_type_count = Counter(
        project['project_type'] for project in projects)

    # Converting the counter to a dictionary, if needed
    project_type_count_dict = dict(project_type_count)
    # Colors for the Project_types doughnut chart
    project_type_colors = ["#116DEE", "#EE9211",
                           "#6346B9", "#9CB946", "#B94653"]

    ### DOUGHNUT CHART ###
    # populate the labels and data for doughnut charts
    doughnutChart_labels, doughnutChart_data, doughnutChart_title = [], [], ""
    # extract key-value pair from dictionary
    for key, value in project_type_count_dict.items():
        doughnutChart_labels.append(str(key))
        doughnutChart_data.append(value)
    doughnutChart_title = "No. of Projects"
    # prepare the totals for landing page
    total_planned = round(sum(planned_td), 2)
    total_actuals = round(sum(actuals_td), 2)
    total_gap = total_actuals - total_planned
    spent_percent = 'Overspent' if total_gap >= 0 else 'Underspent'

    profin = FinancialDataModel.find_by_project_id_and_minor_head(
        selected_year, selected_project)
    all_mom = []
    for month in twelve_months:
        monthly_expense = {}
        monthly_expense['cumm_planned'] = 0
        monthly_expense['cumm_actuals'] = 0
        for row in profin:
            if (row['month_year'].strftime('%b') == month['short_month']):
                monthly_expense['month_year'] = row['month_year'].strftime('%b-%y')
                if (row['minor_head'].upper() == "FIXED COST"):
                    monthly_expense['fc_planned'] = row['planned']
                    monthly_expense['fc_actuals'] = row['actuals']
                if (row['minor_head'].upper() == "ACTIVITIES"):
                    monthly_expense['ac_planned'] = row['planned']
                    monthly_expense['ac_actuals'] = row['actuals']
                if (row['minor_head'].upper() == "OBLIGO"):
                    monthly_expense['ob_planned'] = row['planned']
                    monthly_expense['ob_actuals'] = row['actuals']
                if (row['minor_head'].upper() == "RUNNING COST"):
                    monthly_expense['rc_planned'] = row['planned']
                    monthly_expense['rc_actuals'] = row['actuals']
        all_planned = monthly_expense['fc_planned'] \
                + monthly_expense['ac_planned'] \
                + monthly_expense['ob_planned'] \
                + monthly_expense['rc_planned']
        all_actuals= monthly_expense['fc_actuals'] \
                + monthly_expense['ac_actuals'] \
                + monthly_expense['ob_actuals'] \
                + monthly_expense['rc_actuals']
        if (len(all_mom) == 0):
            monthly_expense['cumm_planned'] = all_planned
            monthly_expense['cumm_actuals'] = all_actuals
        else:
            monthly_expense['cumm_planned'] = all_mom[len(all_mom)-1]['cumm_planned'] \
            + all_planned
            monthly_expense['cumm_actuals'] = all_mom[len(all_mom)-1]['cumm_actuals'] \
            + all_actuals
        all_mom.append(monthly_expense)

    # arrays to store data for the whole calendar year
    fixed_cost, running_cost, activities_cost, obligos_cost,\
          total_cumm_planned, total_cumm_actuals = [], [], [], [], [], []

    for idx, row in enumerate(all_mom):
        if row['fc_actuals'] > 0:
            fixed_cost.append(row['fc_actuals'])
            running_cost.append(row['rc_actuals'])
            activities_cost.append(row['ac_actuals'])
            obligos_cost.append(row['ob_actuals'])
            total_cumm_actuals.append(row['cumm_actuals'])
            total_cumm_planned.append(row['cumm_planned'])
        else:
            fixed_cost.append(row['fc_planned'])
            running_cost.append(row['rc_planned'])
            activities_cost.append(row['ac_planned'])
            obligos_cost.append(row['ob_planned'])


    return render_template('project_financials.html',
                           projects=projects,
                           project=project,
                           financials=year_on_year,
                           filter_year=selected_year,
                           filter_project=selected_project,
                           doughnutChart_labels=doughnutChart_labels,
                           doughnutChart_data=doughnutChart_data,
                           doughnutChart_title=doughnutChart_title,
                           labels_mixed_chart=labels_month,
                           cumm_planned_datalist=cumm_planned_td,
                           cumm_actuals_datalist=cumm_actuals_td,
                           planned_data=planned,
                           actuals_data=actuals,
                           total_planned='{:,.2f}'.format(total_planned),
                           total_actuals='{:,.2f}'.format(total_actuals),
                           total_gap='{:,.2f}'.format(total_gap),
                           spent_percent=spent_percent,
                           pf=month_on_month, project_types=project_type_count_dict,
                           project_type_color=project_type_colors,
                           project_financials=all_mom,
                           fixed_cost=fixed_cost,
                           running_cost = running_cost,
                           activities_cost = activities_cost,
                           obligos_cost = obligos_cost,
                           total_cumm_actuals = total_cumm_actuals,
                           total_cumm_planned = total_cumm_planned)


@blp.route("/projects", methods=['GET', 'POST'])
def projects():
    # Get all projects of NRMAe
    projects = projectDataModel.get_all_projects()
    # datetime.today().strftime('%Y-%m-%d')
    today_date = datetime.datetime.strptime(date.today().strftime('%b-%y'),'%b-%y')
    new_projects = []
    volume = 0
    bilateral_volume = 0
    sewoh_volume = 0
    dpp_volume = 0
    sewoh_numbers = 0    
    bilateral_numbers = 0
    dpp_numbers = 0
    for idx, row in enumerate(projects):
        project_end_date = datetime.datetime.strptime(row['to_date'],'%b-%y')
        project_start_date = datetime.datetime.strptime(row['from_date'],'%b-%y')
        if project_end_date >= today_date and project_start_date <= today_date:
            new_projects.append(row)
            volume = volume + float(row['comm_value'])
            # number_of_projects = number_of_projects + 1
            if row['project_type'].lower() == 'sewoh':
                sewoh_volume = sewoh_volume + float(row['comm_value'])
                sewoh_numbers = sewoh_numbers + 1
            elif row['project_type'].lower()=='bilateral':
                bilateral_volume = bilateral_volume + float(row['comm_value'])
                bilateral_numbers = bilateral_numbers + 1

    unique_types=[]
    for p in projects:
        if p['project_type'] not in unique_types:
            unique_types.append(p['project_type'])

    project_types = []
    for type in unique_types:
        project_type={}
        project_type['project_type']=type.upper()
        project_type['volume'] = 0
        project_type['numbers'] = 0
        for p in new_projects:
            if type.lower() == p['project_type'].lower():
                project_type['volume'] = project_type['volume'] + float(p['comm_value'])
                project_type['numbers'] = project_type['numbers'] + 1
        project_types.append(project_type)
    
    chartdata = {}
    chartdata['types'] = list_to_array('project_type', project_types)
    chartdata['comm_values'] = list_to_array('volume', project_types)
    chartdata['project_numbers'] = list_to_array('numbers', project_types)

    if request.method=='POST':            
        # set the selected project in session
        if "filter_project" in session:
            selected_project = session["filter_project"]
        if "projectName" in request.form:
            selected_project = int(request.form['projectName'])
            session["filter_project"] = selected_project
    else:  # else initiatize the session values
        selected_project = 1
        session["filter_project"] = selected_project
    project_desc = projectDataModel.find_by_id(int(selected_project))

    return render_template('projects.html', projects=new_projects,
                           total_commission=volume/1000000,
                           total_bilateral = bilateral_volume/1000000,
                           total_sewoh = sewoh_volume/1000000,
                           chartdata = chartdata,
                           project_desc = project_desc,
                           filter_project = selected_project)

@blp.route("/dataentry", methods=['GET', 'POST'])
@blp.arguments(FinancialDataSchema)
def dataentry(self):
    message = 'False'
    projects = projectDataModel.get_all_projects()
    twelve_months = get_calendar_months()
    current_year = datetime.datetime.today().year
    dd_months=[]
    for i in twelve_months: 
        dd_months.append(i['short_month'] + '-' + str(current_year))
    if request.method=='POST':
    #if "project_id" in request.form:
        jsonData = request.get_json()
        _projects_id = request.form['project_id']
        _month_year = datetime.datetime.strptime(request.form['month_year'],'%b-%Y')
        _activities = request.form['ac_actuals']
        _obligo = request.form['ob_actuals']
        _running_cost = request.form['rc_actuals']
        _fixed_cost = request.form['fc_actuals']
        _vgk = request.form['vgk']
        _others = request.form['advances']
        message = FinancialDataModel.save_project_financials(_projects_id, _month_year, _activities, _obligo, _running_cost, _fixed_cost, _vgk, _others)

    return render_template('de_financials.html', projects =  projects, dd_months=dd_months, message=message)

def list_to_array(column_name, object_list):
    column_list =[]
    for row in object_list:
        column_list.append(row[column_name])
    return column_list

def get_calendar_months():
    twelve_months = []
    for i in range(1, 13):
        year = date.today().year
        temp_date = date(year, i, 1)
        single_month = {}
        single_month['int_month'] = temp_date.strftime('%m')
        single_month['short_month'] = temp_date.strftime('%b')
        single_month['long_month'] = temp_date.strftime('%B')
        twelve_months.append(single_month)
    return twelve_months


#{'planned': 0, 'actuals': '300', 'projects_id': '34', 'month_year': datetime.datetime(20..., 1, 0, 0), 'minor_head': 'Activities'}
