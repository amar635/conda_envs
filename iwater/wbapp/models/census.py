from wbapp.db_sqlalchemy import db

class CensusDatum(db.Model):
    __tablename__ = 'census_data'

    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('census_data_id_seq'::regclass)"))
    total_geographical_area = db.Column(db.Float(53), server_default=db.text("0"))
    households = db.Column(db.Integer, server_default=db.text("0"))
    male_population = db.Column(db.Integer, server_default=db.text("0"))
    female_population = db.Column(db.Integer, server_default=db.text("0"))
    sc_population = db.Column(db.Float(53), server_default=db.text("0"))
    st_population = db.Column(db.Float(53), server_default=db.text("0"))
    forest_area = db.Column(db.Float(53), server_default=db.text("0"))
    non_agricultural_area = db.Column(db.Float(53), server_default=db.text("0"))
    uncultivable_land_area = db.Column(db.Float(53), server_default=db.text("0"))
    grazing_land_area = db.Column(db.Float(53), server_default=db.text("0"))
    misc_crops_area = db.Column(db.Float(53), server_default=db.text("0"))
    wasteland_area = db.Column(db.Float(53), server_default=db.text("0"))
    fallows_land_area = db.Column(db.Float(53), server_default=db.text("0"))
    current_fallows_area = db.Column(db.Float(53), server_default=db.text("0"))
    unirrigated_land_area = db.Column(db.Float(53), server_default=db.text("0"))
    canals_area = db.Column(db.Float(53), server_default=db.text("0"))
    tubewell_area = db.Column(db.Float(53), server_default=db.text("0"))
    tank_lake_area = db.Column(db.Float(53), server_default=db.text("0"))
    waterfall_area = db.Column(db.Float(53), server_default=db.text("0"))
    other_sources_area = db.Column(db.Float(53), server_default=db.text("0"))
    village_id = db.Column(db.ForeignKey('villages.id'), nullable=False)

    village = db.relationship('Village')