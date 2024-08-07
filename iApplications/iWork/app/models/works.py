from sqlalchemy import and_, select
from iWork.app.classes.helper_methods import Helper
from iWork.app.db import db
from iWork.app.models import Panchayat, WorkType, Block, District, State

class Work(db.Model):
    __tablename__ = 'nrega_works'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(50))
    name = db.Column(db.String(500))
    amount_sanctioned = db.Column(db.Float)
    amoung_spent = db.Column(db.Float)
    person_days = db.Column(db.Integer)
    start_date = db.Column(db.String(100))
    end_date = db.Column(db.String(100))
    fin_year = db.Column(db.String(50))
    work_type = db.column(db.String(500))
    category_id = db.Column(db.ForeignKey('categories_master.id'), nullable=False)
    panchayat_id = db.Column(db.ForeignKey('nrega_panchayats.id'), nullable=False)

    panchayat = db.relationship('Panchayat')
    category = db.relationship('Category')

    def __init__(self, code, name, amount_sanctioned, amount_spent, person_days, 
                 start_date, end_date, fin_year, work_type, category_id,panchayat_id ):
        self.code = code
        self.name = name
        self.amount_sanctioned = amount_sanctioned
        self.amoung_spent = amount_spent
        self.person_days = person_days
        self.start_date = start_date
        self.end_date = end_date
        self.fin_year = fin_year
        self.work_type = work_type
        self.category_id = category_id
        self.panchayat_id = panchayat_id

    def json(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'amount_sanctioned': self.amount_sanctioned,
            'amount_spent': self.amoung_spent,
            'person_days':self.panchayat_id,
            'start_date':self.start_date,
            'end_date': self.end_date,
            'fin_year': self.fin_year,
            'work_type': self.work_type,
            'category_id': self.category_id,
            'panchyat_id': self.panchayat_id
        }
    
    @classmethod
    def get_assets_by_panchayat_id(cls, panchayat_id):
        from iWork.app.models import AssetData
        # Subquery to get asset_ids from assets_data where panchayat_id = 2427
        subquery = db.session.query(AssetData.asset_id).filter(AssetData.panchayat_id == panchayat_id).subquery()
        # Explicitly convert the subquery to a select() construct
        subquery_select = select(subquery)

        # Main query
        query = db.session.query(
                cls.id.label('id'),
                cls.asset_id.label('asset_id')
                ).filter(
                and_(
                    cls.id.notin_(subquery_select),
                    cls.panchayat_id == panchayat_id
                )
            )
        # query = db.session.query(
        #         cls.id.label('id'),
        #         cls.asset_id.label('asset_id')
        #     ).join(Panchayat, Panchayat.id == Asset.panchayat_id
        #     ).join(Block, Block.id == Panchayat.block_id
        #     ).join(District, District.id == Block.district_id
        #     ).join(State, State.id == District.state_id
        #     ).filter(Asset.panchayat_id == panchayat_id
        #     )
        results = query.all()
        json_data = [{'id': result[0],'asset_id':result[1]} for result in results]
        json_data = sorted(json_data, key=lambda x: x['asset_id'])
        return json_data

    @classmethod
    def get_assets_by_id(cls, id):
        query = db.session.query(
                    cls.work_code.label('work_code'),
                    WorkType.name.label('work_type'),
                    cls.cost.label('asset_cost'),
                    cls.photo_url.label('photo_url')
                    ).join(
                        WorkType, cls.work_type_id == WorkType.id
                    ).filter(cls.id == id)
        
        results = query.first()
        json_data = {'work_code': results[0],'work_type': results[1],'asset_cost':results[2],'photo_url':results[3]} 
        return json_data

    @classmethod
    def get_states(cls):
        query = db.session.query(
                    cls.panchayat_id.label('panchayat_id'),
                    State.id.label('id'),
                    State.name.label('name')
                    ).join(
                        Panchayat, cls.panchayat_id == Panchayat.id
                    ).join(
                        Block, Panchayat.block_id == Block.id
                    ).join(
                        District, Block.district_id == District.id
                    ).join(
                        State, District.state_id == State.id
                    ).distinct()
        
        results = query.all()
        json_data = Helper.remove_duplicates([{'id': result[1], 'name': result[2]} for result in results])
        json_data = sorted(json_data, key=lambda x: x['name'])
        return json_data

    @classmethod
    def get_districts_by_state_id(cls, state_id):
        query = db.session.query(
                    cls.panchayat_id.label('panchayat_id'),
                    District.id.label('id'),
                    District.name.label('name')
                    ).join(
                        Panchayat, cls.panchayat_id == Panchayat.id
                    ).join(
                        Block, Panchayat.block_id == Block.id
                    ).join(
                        District, Block.district_id == District.id
                    ).join(
                        State, District.state_id == State.id
                    ).filter(State.id == state_id)
        
        results = query.all()
        json_data = Helper.remove_duplicates([{'id': result[1], 'name': result[2]} for result in results])
        json_data = sorted(json_data, key=lambda x: x['name'])
        return json_data

    @classmethod
    def get_blocks_by_district_id(cls, district_id):
        query = db.session.query(
                    cls.panchayat_id.label('panchayat_id'),
                    Block.id.label('id'),
                    Block.name.label('name')
                    ).join(
                        Panchayat, cls.panchayat_id == Panchayat.id
                    ).join(
                        Block, Panchayat.block_id == Block.id
                    ).join(
                        District, Block.district_id == District.id
                    ).join(
                        State, District.state_id == State.id
                    ).filter(District.id == district_id)
        
        results = query.all()
        json_data = Helper.remove_duplicates([{'id': result[1], 'name': result[2]} for result in results])
        json_data = sorted(json_data, key=lambda x: x['name'])
        return json_data

    @classmethod
    def get_panchayats_by_block_id(cls, block_id):
        query = db.session.query(
                    cls.panchayat_id.label('panchayat_id'),
                    Panchayat.id.label('id'),
                    Panchayat.name.label('name')
                    ).join(
                        Panchayat, cls.panchayat_id == Panchayat.id
                    ).join(
                        Block, Panchayat.block_id == Block.id
                    ).join(
                        District, Block.district_id == District.id
                    ).join(
                        State, District.state_id == State.id
                    ).filter(Block.id == block_id)
        
        results = query.all()
        json_data = Helper.remove_duplicates([{'id': result[1], 'name': result[2]} for result in results])
        json_data = sorted(json_data, key=lambda x: x['name'])
        return json_data
    
