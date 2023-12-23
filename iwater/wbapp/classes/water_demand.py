import json
from flask import jsonify
from wbapp.models.livestock_census import LivestockCensus
from wbapp.models.census import CensusDatum


class WaterDemand:

    def __init__(self, village_id):
        self.agricuture = self.agriculture_consumption(village_id)
        self.human = self.human_consumption(village_id)
        self.livestock = self.livestock_consumption(village_id)

    def agricuture_consumption(json_data):
        census = CensusDatum.get_census_data(json_data)
        # census = CensusDatum.get_by_village(village_id=village_id)
        irrigated = census.canals_area + census.tubewell_area + census.tank_lake_area + census.waterfall_area + census.other_sources_area
        rainfed = census.unirrigated_land_area + census.current_fallows_area + irrigated
        agriculture = []
        agriculture.append({'type': 'irrigated', 'quantity' : round(irrigated,1), 'demand': round(irrigated * 0.8, 1), 'deno': 'area'})
        agriculture.append({'type': 'rainfed', 'quantity' : round(rainfed,1), 'demand': round(rainfed * 0.2, 1), 'deno': 'area'})
        return agriculture

    def human_consumption(json_data):
        census = CensusDatum.get_census_data(json_data)
        # census = CensusDatum.get_by_village(village_id=village_id)
        # print(census)
        male = census.male_population 
        female = census.female_population
        human = []
        human.append({'type': 'male', 'quantity' : male, 'demand': round(male * 27.375/10000,1), 'deno':'numbers'})
        human.append({'type': 'female', 'quantity' : female, 'demand': round(female * 27.375/10000, 1),'deno':'numbers'})
        return human
    
    def livestock_consumption(json_data):
        livestocks = []
        livestock_census = LivestockCensus.get_livestock_census(json_data=json_data)
        for item in livestock_census:
            livestocks.append({'type':item[1],'quantity':int(item[2]), 'demand':round(float(item[3]/10000) * int(item[2]),2), 'deno': 'numbers'})
        return livestocks

