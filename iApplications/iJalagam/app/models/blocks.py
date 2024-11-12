from sqlalchemy import and_
from iJalagam.app.db import db
from iJalagam.app.models import District, State

class Block(db.Model):
    __tablename__ = 'blocks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.Integer, nullable=False)
    census_code = db.Column(db.Integer)
    district_id = db.Column(db.ForeignKey('districts.id'), nullable=False)
    state_id = db.Column(db.ForeignKey('states.id'), nullable=False)
    local_name = db.Column(db.String(100))

    district = db.relationship('District')
    state = db.relationship('State')

    def __init__(self, name, code, census_code, district_id, state_id, local_name):
        self.name = name
        self.code = code
        self.census_code = census_code
        self.district_id = district_id
        self.state_id = state_id
        self.local_name = local_name


    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'census_code': self.census_code,
            'district_id': self.district_id,
            'state_id': self.state_id,
            'local_name': self.local_name
        }


    @classmethod
    def get_blocks(cls, district_id):
        results = cls.query.filter_by(district_id = district_id).order_by(cls.name).all()
        if results:
            json_data = [result.json() for result in results]
            return json_data
        else:
            return None
    
    @classmethod
    def get_district_by_block(cls, block_id):
        return cls.query.filter_by(id = block_id).first()
    
    @classmethod
    def get_id_and_name(cls, block_id, district_id, state_id):
        query = db.session.query(
            cls.id.label('block_id'),
            cls.name.label('block_name'),
            District.id.label('district_id'),
            District.name.label('district_name'),
            State.id.label('state_id'),
            State.name.label('state_name'),
        ).join(District, District.id == cls.district_id
        ).join(State, State.id == District.state_id
        ).filter(and_(Block.id == block_id, District.id==district_id))

        result = query.first()

        if result:
            json_data = {'block':{'id':result[0], 'name': result[1]},
                         'district':{'id':result[2], 'name': result[3]},
                         'state':{'id':result[4], 'name': result[5]},}
            return json_data
        else:
            return None