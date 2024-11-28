from datetime import datetime

from sqlalchemy import func
from iJalagam.app import db


class WaterTransfer(db.Model):
    __tablename__ = "water_transfers"

    id = db.Column(db.Integer, primary_key=True)
    allottee = db.Column(db.String(80))
    annual_allocation = db.Column(db.Float, nullable=False, default=0)
    measuring_unit = db.Column(db.String(50))
    created_by = db.Column(db.ForeignKey('users.id'), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now)
    block_id = db.Column(db.ForeignKey('blocks.id'), nullable=False)
    district_id = db.Column(db.ForeignKey('districts.id'), nullable=False)

    block = db.relationship('Block')
    district = db.relationship('District')
    user = db.relationship('User')

    def __init__(self, allottee, annual_allocation, measuring_unit, created_by, block_id, district_id):
        self.allottee = allottee
        self.annual_allocation = annual_allocation
        self.measuring_unit = measuring_unit
        self.created_by = created_by
        self.block_id = block_id
        self.district_id = district_id

    def json(self):
        return {
            'id': self.id,
            'allottee': self.allottee,
            'annual_allocation': self.annual_allocation,
            'measuring_unit': self.measuring_unit,
            'created_by': self.created_by,
            'created_on': self.created_on,
            'block_id': self.block_id,
            'district_id': self.district_id
        }
    
    @classmethod
    def get_water_transfer(cls, transfer_description, block_id, district_id ):
        return cls.query.filter(func.lower(cls.allottee)==transfer_description.lower(),
                                   cls.block_id==block_id,
                                   cls.district_id==district_id).first()
    
    def update_to_db(self):
        # db.session.update(self)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()