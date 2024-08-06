from iWork.app.db import db
from iWork.app.models import Asset, ProposedStatus

class AssetData(db.Model):
    __tablename__ = 'assets_data'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    input_value = db.Column(db.String(100))
    asset_id = db.Column(db.ForeignKey('nrega_assets.id'), nullable=False)
    proposed_status_id = db.Column(db.ForeignKey('proposed_status_master.id'), nullable=False)
    input_id = db.Column(db.ForeignKey('input_parameters_master.id'), nullable=False)
    panchayat_id = db.Column(db.ForeignKey('nrega_panchayats.id'), nullable=False)

    proposed_status = db.relationship('ProposedStatus')
    asset = db.relationship('Asset')
    input_parameter = db.relationship('InputParameter')
    panchayat = db.relationship('Panchayat')

    def __init__(self, input_value, asset_id, proposed_status_id, input_id, panchayat_id):
        self.input_value = input_value
        self.asset_id = asset_id
        self.proposed_status_id = proposed_status_id
        self.input_id = input_id
        self.panchayat_id = panchayat_id

    def json(self):
        return {
            'id': self.id,
            'asset_id': self.asset_id,
            'proposed_status_id': self.proposed_status_id,
            'input_id':self.input_id,
            'panchayat_id': self.panchayat_id
        }
    
    @classmethod
    def get_all(cls):
        query=cls.query.order_by(cls.asset_id)
        return query

    @classmethod
    def get_assets_by_panchayat(cls, panchayat_id):
        results = cls.query.filter(cls.panchayat_id==panchayat_id).all()
        if results:
            assets_by_panchayat = []
            for result in results:
                assets_by_panchayat.append(result.json())
            return assets_by_panchayat
        else:
            return None
    
    @classmethod
    def get_asset_data_by_panchayat(cls, panchayat_id):
        results = db.session.query(
            cls.asset_id.label('asset_id'),
            cls.proposed_status_id.label('proposed_status_id'),
            Asset.asset_id.label('bhuvan_asset_id'),
            ProposedStatus.proposed_status.label('proposed_status')
        ).join(Asset, Asset.id ==cls.asset_id
        ).join(ProposedStatus, ProposedStatus.id == cls.proposed_status_id            
        ).filter(cls.panchayat_id==panchayat_id).all()
        if results:
            assets_by_panchayat = [{ 
                                    'asset_id':result.asset_id, 
                                    'proposed_status_id':result.proposed_status_id,
                                    'bhuvan_asset_id':result.bhuvan_asset_id,
                                    'proposed_status':result.proposed_status}for result in results]
            return assets_by_panchayat
        else:
            return None
        
    @classmethod
    def get_asset_data_by_id(cls, asset_id):
        return None
        # results = db.session.query(

        # ).join(Asset,

        # ).join(

        # ).filter()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete_from_db(cls, _id):
        asset_data = cls.query.filter_by(id=_id).first()
        db.session.delete(asset_data)
        db.session.commit()

    def commit_db():
        db.session.commit()
    
    @classmethod
    def update_db(cls, data,_id):
        asset_data = cls.query.filter_by(id=_id).update(data)
        db.session.commit()