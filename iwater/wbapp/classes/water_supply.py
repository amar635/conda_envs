from wbapp.models.strange_table import StrangeRunoff
from wbapp.models.census import CensusDatum
from wbapp.models.waterbody import Waterbody


class WaterSupply:

    def __init__(self):
        pass

    def get_available_runoff(village_id):
        census = CensusDatum.get_by_village(village_id=village_id)
        good_catchment_area = census.forest_area + census.non_agricultural_area + census.uncultivable_land_area
        average_catchment_area = census.grazing_land_area + census.misc_crops_area + census.wasteland_area
        irrigated_area = census.canals_area + census.tubewell_area + census.tank_lake_area + census.waterfall_area + census.other_sources_area
        bad_catchment_area = census.fallows_land_area + census.current_fallows_area + census.unirrigated_land_area + irrigated_area
        runoff = StrangeRunoff.get_runoff_yield(760)
        water_resources = {'good': round((good_catchment_area/100) * runoff['good'],2),
                           'average': round((average_catchment_area/100) * runoff['average'],2),
                           'bad': round((bad_catchment_area/100) * runoff['bad'],2)}
        return water_resources
    
    def get_harvested_runoff(village_id):
        harvested_runoff = []
        waterbodies = Waterbody.get_waterbodies(village_ids=[village_id])
        for item in waterbodies:
            harvested_runoff.append({'area': round(float(item[0]),2), 'waterbody':item[1]})
        return harvested_runoff