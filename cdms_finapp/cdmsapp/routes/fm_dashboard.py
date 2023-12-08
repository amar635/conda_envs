from collections import Counter
from datetime import date
import html
from flask import render_template, request, session
from flask_smorest import Blueprint, abort

from cdmsapp.models import projectDataModel, pywfModel, FinancialDataModel
# blp = Blueprint("dashboard", "dashboards",
#                 description="html pages for financial dashboard")


# @blp.route("/dashboard", methods=['GET', 'POST'])
# def filters():
#     if request.method == 'POST':
#         if "filter_project" in session:
#             selectedProjectId = session["filter_project"]
#         if "filter_year" in session:
#             selectedYear = session["filter_year"]
#         if "filter_month" in session:
#             selectedMonth = session["filter_month"]
#         # Selected project function and methods
#         if "projectName" in request.form:
#             selectedProjectId = int(request.form['projectName'])
#             session["filter_project"] = selectedProjectId
#         # Selected year functions and methods
#         if "projectYear" in request.form:
#             selectedYear = int(request.form['projectYear'])
#             session["filter_year"] = selectedYear
#         # Selected month functions and methods
#         # if 'projectMonth' in request.form:
#         #     selectedMonth = request.form['projectMonth']

#     else:
#         selectedProjectId = 1
#         session["filter_project"] = selectedProjectId
#         selectedYear = date.today().year
#         session["filter_year"] = selectedYear
#         selectedMonth = 1
#         session["filter_month"] = selectedMonth

#     # get all the projects from projectDataModel with entities
#     projects = projectDataModel.query.with_entities(projectDataModel.shortname, projectDataModel.id) \
#         .order_by(projectDataModel.shortname).all()
#     # session["projects"] = projects
#     project = projectDataModel.find_by_id(int(selectedProjectId))
#     # session["project_detail"] = project
#     pywf = pywfModel.find_by_projects_id(selectedProjectId)
#     year_on_year = []
#     hasYoyData = False
#     if len(pywf) > 0:
#         column_names = pywf[0].__table__.columns.keys()
#         if len(column_names) > 0:
#             hasYoyData = True
#             for i in range(len(column_names)):
#                 if(i > 2):
#                     if(column_names[i] != 'projects_id'):
#                         row = {}
#                         row['description'] = column_names[i]
#                         for j in range(len(pywf)):
#                             row[str(getattr(pywf[j], 'year'))] = getattr(
#                                 pywf[j], column_names[i])
#                         year_on_year.append(row)
#     # session["year_on_year"] = year_on_year
#     pf = FinancialDataModel.find_by_project_id_and_year(
#         selectedYear, selectedProjectId)
#     # Chart data for representation
#     twelve_months = get_calendar_months()
#     labels, planned_data, actuals_data, cumm_planned_datalist, cumm_actuals_datalist = [], [], [], [], []
#     for mon in twelve_months:
#         planned_ = 0
#         actuals_ = 0
#         cumm_planned_ = 0
#         cumm_actuals_ = 0
#         for row in pf:
#             if (row['month_year'].strftime('%b') == mon['short_month']):
#                 planned_ = round(row['planned'], 2)
#                 actuals_ = round(row['actuals'], 2)
#                 # row['cumm_planned'] =
#         planned_data.append(planned_)
#         actuals_data.append(actuals_)
#         if len(cumm_planned_datalist) == 0:
#             cumm_planned_ = planned_
#             cumm_actuals_ = actuals_
#         else:
#             cumm_planned_ = round(cumm_planned_datalist[len(
#                 cumm_planned_datalist)-1] + planned_, 2)
#             cumm_actuals_ = round(cumm_actuals_datalist[len(
#                 cumm_actuals_datalist)-1] + actuals_, 2)
#         cumm_planned_datalist.append(cumm_planned_)
#         cumm_actuals_datalist.append(cumm_actuals_)
#         labels.append(mon['short_month'])
#         if actuals_ > 0:
#             curr_month = mon['long_month'] + "-" + str(selectedYear)
#         else:
#             curr_month = "No Data"

#     total_planned = round(sum(planned_data), 2)
#     total_actuals = round(sum(actuals_data), 2)
#     spent_percent, progress_width = "", ""
#     hasFinData = False
#     if total_planned > 0:
#         spent_percent = "{0:.0%}".format(round(total_actuals/total_planned, 2))
#         if ((total_actuals/total_planned)*100) < 0:
#             spent_percent = "{0:.2%}".format(
#                 round(total_actuals/total_planned, 4))
#         progress_width = "width: " + str(spent_percent)
#         hasFinData = True

#     return render_template(template_name_or_list='dashboard.html',
#                            project=project, data=projects, financials=year_on_year,
#                            pf=pf, filter_year=selectedYear, filter_month=selectedMonth,
#                            filter_project_id=selectedProjectId, chart_labels=labels,
#                            chart_planned=planned_data, chart_actuals=actuals_data,
#                            chart_cumm_planned=cumm_planned_datalist, chart_cumm_actuals=cumm_actuals_datalist,
#                            total_planned=total_planned, total_actuals=total_actuals,
#                            spent_percent=spent_percent, progress_width=progress_width,
#                            curr_month=curr_month, showFinData=hasFinData, showYoy=hasYoyData)


# @blp.route("/db_crud", methods=['GET', 'POST'])
# def crud():
#     # 3A517F,#A6ABBD,#727787,#7D3E4A,#B46F7A
#     # if the page is submitted capture the project or year in the sesssion
#     if request.method == 'POST':
#         if "filter_project" in session:
#             selected_project = session["filter_project"]
#         if "filter_year" in session:
#             selected_year = session["filter_year"]
#         # Selected project function and methods
#         if "projectName" in request.form:
#             selected_project = int(request.form['projectName'])
#             session["filter_project"] = selected_project
#         # Selected year functions and methods
#         if "projectYear" in request.form:
#             selected_year = int(request.form['projectYear'])
#             session["filter_year"] = selected_year
#     else:  # else initiate the session values
#         selected_project = 1
#         session["filter_project"] = selected_project
#         selected_year = date.today().year
#         session["filter_year"] = selected_year

#     # Get all projects of NRMAe
#     projects = projectDataModel.get_all_projects()
#     # get specific project requirement
#     project = projectDataModel.find_by_id(int(selected_project))
#     # get project financials - month wise planned and actual expenses of the project
#     project_financials = FinancialDataModel.find_by_project_id_and_year(
#         selected_year, selected_project)

#     # make the financial data table with cummulatives and gaps
#     month_on_month = []
#     twelve_months = get_calendar_months()
#     for row in project_financials:
#         monthly_expenses = {}
#         for mon in twelve_months:
#             if (row['month_year'].strftime('%b') == mon['short_month']):
#                 monthly_expenses['month_only'] = mon['short_month']
#                 monthly_expenses['month_year'] = row['month_year']
#                 monthly_expenses['planned'] = round(row['planned'], 2)
#                 monthly_expenses['actuals'] = round(row['actuals'], 2)
#                 monthly_expenses['gap'] = monthly_expenses['actuals'] - \
#                     monthly_expenses['planned']
#                 monthly_expenses['percent'] = monthly_expenses['gap']/monthly_expenses['planned']
#                 if (len(month_on_month) == 0):
#                     monthly_expenses['cumm_planned'] = monthly_expenses['planned']
#                     monthly_expenses['cumm_actuals'] = monthly_expenses['actuals']
#                 else:
#                     monthly_expenses['cumm_planned'] = month_on_month[len(
#                         month_on_month)-1]['cumm_planned']+monthly_expenses['planned']
#                     monthly_expenses['cumm_actuals'] = month_on_month[len(
#                         month_on_month)-1]['cumm_actuals'] + monthly_expenses['actuals']
#                 monthly_expenses['cumm_gap'] = monthly_expenses['cumm_actuals'] - \
#                     monthly_expenses['cumm_planned']
#                 monthly_expenses['cumm_percent'] = monthly_expenses['cumm_gap']/monthly_expenses['cumm_planned']
#                 break
#         if monthly_expenses:
#             month_on_month.append(monthly_expenses)
#     # prepare mixed chart labels and dataset]
#     # arrays to store data for the whole calendar year
#     labels_month, planned, actuals, cumm_planned, cumm_actuals = [], [], [], [], []
#     # arrays to store data till date (hence td)
#     labels_td, planned_td, actuals_td, cumm_planned_td, cumm_actuals_td = [], [], [], [], []
#     for idx, row in enumerate(month_on_month):
#         # fill the dataset and labels for the whole calendar year
#         labels_month.append(row['month_only'])
#         planned.append(row['planned'])
#         actuals.append(row['actuals'])
#         cumm_planned.append(row['cumm_planned'])
#         cumm_actuals.append(row['cumm_actuals'])
#         # fill the dataset and labels array till the current month
#         if idx == 0:
#             labels_td.append(row['month_only'])
#             planned_td.append(row['planned'])
#             actuals_td.append(row['actuals'])
#             cumm_planned_td.append(row['cumm_planned'])
#             cumm_actuals_td.append(row['cumm_actuals'])
#         elif (month_on_month[idx-1]['cumm_actuals'] < row['cumm_actuals']):
#             labels_td.append(row['month_only'])
#             planned_td.append(row['planned'])
#             actuals_td.append(row['actuals'])
#             cumm_planned_td.append(row['cumm_planned'])
#             cumm_actuals_td.append(row['cumm_actuals'])
#     # get project year on year data and transpose it for display
#     pywf = pywfModel.find_by_projects_id(selected_project)
#     year_on_year = []
#     hasYoyData = False
#     if len(pywf) > 0:
#         column_names = pywf[0].__table__.columns.keys()
#         if len(column_names) > 0:
#             hasYoyData = True
#             for i in range(len(column_names)):
#                 if(i > 2):
#                     if(column_names[i] != 'projects_id'):
#                         row = {}
#                         row['description'] = column_names[i]
#                         for j in range(len(pywf)):
#                             row[str(getattr(pywf[j], 'year'))] = getattr(
#                                 pywf[j], column_names[i])
#                         year_on_year.append(row)
#     # create an array with count project['projectType'] from the list of project
#     # Using the Counter class from the collections module to count the project types
#     project_type_count = Counter(
#         project['project_type'] for project in projects)

#     # Converting the counter to a dictionary, if needed
#     project_type_count_dict = dict(project_type_count)
#     # Colors for the Project_types doughnut chart
#     project_type_colors = ["#116DEE", "#EE9211",
#                            "#6346B9", "#9CB946", "#B94653"]

#     ### DOUGHNUT CHART ###
#     # populate the labels and data for doughnut charts
#     doughnutChart_labels, doughnutChart_data, doughnutChart_title = [], [], ""
#     # extract key-value pair from dictionary
#     for key, value in project_type_count_dict.items():
#         doughnutChart_labels.append(str(key))
#         doughnutChart_data.append(value)
#     doughnutChart_title = "No. of Projects"
#     # prepare the totals for landing page
#     total_planned = round(sum(planned_td), 2)
#     total_actuals = round(sum(actuals_td), 2)
#     total_gap = total_actuals - total_planned
#     spent_percent = 'Overspent' if total_gap > 0 else 'Underspent'
#     ### LINE & BAR MIXED CHART ###
#     # twelve_months = get_calendar_months()
#     # labels_mixed_chart, planned_data, actuals_data, cumm_planned_datalist, cumm_actuals_datalist, \
#     #     cumm_actuals_chartdata, cumm_planned_chartdata = [], [], [], [], [], [], []
#     # for mon in twelve_months:
#     #     planned_ = 0
#     #     actuals_ = 0
#     #     cumm_planned_ = 0
#     #     cumm_actuals_ = 0
#     #     for row in project_financials:
#     #         if (row['month_year'].strftime('%b') == mon['short_month']):
#     #             planned_ = round(row['planned'], 2)
#     #             actuals_ = round(row['actuals'], 2)
#     #             # row['cumm_planned'] =
#     #     planned_data.append(planned_)
#     #     actuals_data.append(actuals_)
#     #     if len(cumm_planned_datalist) == 0:
#     #         cumm_planned_ = planned_
#     #         cumm_actuals_ = actuals_
#     #     else:
#     #         cumm_planned_ = round(cumm_planned_datalist[len(
#     #             cumm_planned_datalist)-1] + planned_, 2)
#     #         cumm_actuals_ = round(cumm_actuals_datalist[len(
#     #             cumm_actuals_datalist)-1] + actuals_, 2)
#     #     cumm_planned_datalist.append(cumm_planned_)
#     #     cumm_actuals_datalist.append(cumm_actuals_)
#     #     if len(cumm_actuals_datalist)-1 == 0:  # Enter the first record as it is
#     #         cumm_actuals_chartdata.append(cumm_actuals_)
#     #         cumm_planned_chartdata.append(cumm_planned_)
#     #     elif ((cumm_actuals_datalist[len(cumm_actuals_datalist)-2] < cumm_actuals_datalist[len(cumm_actuals_datalist)-1]) or (cumm_actuals_ == 0)):
#     #         cumm_actuals_chartdata.append(cumm_actuals_)
#     #         cumm_planned_chartdata.append(cumm_planned_)
#     #     labels_mixed_chart.append(mon['short_month'])

#     # if total_planned> 0:
#     #     percent_change = (total_actuals/total_planned) * 100
#     #     if(percent_change < 0):
#     #         spent_percent="{0:.0%}".format(round(percent_change,2))
#     #     else:
#     #         spent_percent="{0:.2%}".format(round(percent_change,4))

#     return render_template('project_financials.html',
#                            projects=projects,
#                            project=project,
#                            financials=year_on_year,
#                            filter_year=selected_year,
#                            filter_project=selected_project,
#                            doughnutChart_labels=doughnutChart_labels,
#                            doughnutChart_data=doughnutChart_data,
#                            doughnutChart_title=doughnutChart_title,
#                            labels_mixed_chart=labels_month,
#                            cumm_planned_datalist=cumm_planned_td,
#                            cumm_actuals_datalist=cumm_actuals_td,
#                            planned_data=planned,
#                            actuals_data=actuals,
#                            total_planned='{:,.2f}'.format(total_planned),
#                            total_actuals='{:,.2f}'.format(total_actuals),
#                            total_gap='{:,.2f}'.format(total_gap),
#                            spent_percent=spent_percent,
#                            pf=month_on_month, project_types=project_type_count_dict,
#                            project_type_color=project_type_colors)


# def get_calendar_months():
#     twelve_months = []
#     for i in range(1, 13):
#         year = date.today().year
#         temp_date = date(year, i, 1)
#         single_month = {}
#         single_month['int_month'] = temp_date.strftime('%m')
#         single_month['short_month'] = temp_date.strftime('%b')
#         single_month['long_month'] = temp_date.strftime('%B')
#         twelve_months.append(single_month)
#     return twelve_months
