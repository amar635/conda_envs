# from datetime import datetime
from sqlalchemy import and_, func
from iWater.app.db import db

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
    def get_rainfall(cls, district_id, year):
        rainfall_data =  db.session.query(
            func.sum(cls.actual).label('actual'), 
            func.sum(cls.normal).label('normal'))\
            .filter(and_(cls.district_id==district_id,func.extract('year', cls.observation_date).label('year')==year))\
            .group_by(cls.district_id).first()
        return rainfall_data.actual
       