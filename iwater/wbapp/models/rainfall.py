# from datetime import datetime
from wbapp.db_sqlalchemy import db

class RainfallDatum(db.Model):
    __tablename__ = 'rainfall_data'

    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('rainfall_data_id_seq'::regclass)"))
    observation_date = db.Column(db.DateTime)
    normal = db.Column(db.Float(53), nullable=False)
    actual = db.Column(db.Float(53), nullable=False)
    district_id = db.Column(db.ForeignKey('districts.id'), nullable=False)

    district = db.relationship('District')

    def json(self):
        return {
            'id': self.id,
            'observation_data': self.observation_date,
            'normal': self.normal,
            'actual': self.actual,
            'district_id': self.district_id 
        }
    
    @classmethod
    def get_rainfall(cls, json_data):
        rainfall = 760
        return rainfall