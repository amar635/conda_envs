import json
from flask import jsonify
from wbapp.models.livestock_census import LivestockCensus
from wbapp.models.census import CensusDatum


class WaterDemand:

    def __init__(self, village_id):
        self.agricuture = self.agriculture_consumption(village_id)
        self.human = self.human_consumption(village_id)
        self.livestock = self.livestock_consumption(village_id)

    def agricuture_consumption(village_id):
        census = CensusDatum.get_by_village(village_id=village_id)
        irrigated = census.canals_area + census.tubewell_area + census.tank_lake_area + census.waterfall_area + census.other_sources_area
        rainfed = census.unirrigated_land_area + census.current_fallows_area + irrigated
        agriculture = []
        agriculture.append({'type': 'irrigated', 'area' : irrigated, 'demand': irrigated * 0.8})
        agriculture.append({'type': 'rainfed', 'area' : rainfed, 'demand': rainfed * 0.2})
        return agriculture

    def human_consumption(village_id):
        census = CensusDatum.get_by_village(village_id=village_id)
        # print(census)
        male = census.male_population 
        female = census.female_population
        human = []
        human.append({'type': 'male', 'numbers' : male, 'demand': male * 27.375/10000})
        human.append({'type': 'female', 'numbers' : female, 'demand': female * 27.375/10000})
        return human
    
    def livestock_consumption(village_id):
        livestocks_ = []
        livestock_census = LivestockCensus.get_by_village_id(village_id=village_id)
        for item in livestock_census:
            livestocks_.append({'type':item[0],'numbers':int(item[1]),'name':item[5], 'water_use':float(item[4]), 'consumption':float(item[4]) * int(item[1])})
        return livestocks_

