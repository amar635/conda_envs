from collections import defaultdict
from iWork.app.db import db
from iWork.app.models import CompletedWork, PermissibleWork, InputParameter


class FieldData(db.Model):
    __tablename__ = 'field_data'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    input_value = db.Column(db.String(100))
    completed_work_id = db.Column(db.ForeignKey('nrega_completed_works.id'), nullable=False)
    permissible_work_id = db.Column(db.ForeignKey('nrega_permissible_works.id'), nullable=False)
    input_id = db.Column(db.ForeignKey('input_parameters.id'), nullable=False)
    panchayat_id = db.Column(db.ForeignKey('nrega_panchayats.id'), nullable=False)

    permissible_work = db.relationship('PermissibleWork')
    completed_work = db.relationship('CompletedWork')
    input_parameter = db.relationship('InputParameter')
    panchayat = db.relationship('Panchayat')

    def __init__(self, input_value, completed_work_id, permissible_work_id, input_id, panchayat_id):
        self.input_id = input_id
        self.input_value = input_value
        self.completed_work_id = completed_work_id
        self.permissible_work_id = permissible_work_id
        self.panchayat_id = panchayat_id

    def json(self):
        return {
            'id': self.id,
            'input_id':self.input_id,
            'input_value': self.input_value,
            'completed_work_id': self.completed_work_id,
            'permissible_work_id': self.permissible_work_id,
            'panchayat_id': self.panchayat_id
        }
    
    # @classmethod
    # def get_all(cls):
    #     query=cls.query.order_by(cls.asset_id)
    #     return query

    @classmethod
    def get_completed_work_id_by_panchayat(cls, panchayat_id):
        results = db.session.query(cls.completed_work_id).distinct().filter(cls.panchayat_id==panchayat_id).all()
        if results:
            return [{'completed_work_id':result.completed_work_id} for result in results]
        else:
            return None
    
    @classmethod
    def get_field_data_by_panchayat(cls, panchayat_id):
        results = db.session.query(
            cls.id.label('id'),
            InputParameter.name,
            cls.input_value,
            CompletedWork.code.label('work_code'),
            PermissibleWork.permissible_work
        ).join(CompletedWork, CompletedWork.id ==cls.completed_work_id
        ).join(PermissibleWork, PermissibleWork.id == cls.permissible_work_id            
        ).join(InputParameter, InputParameter.id == cls.input_id
        ).filter(cls.panchayat_id==panchayat_id).all()
        if results:
            json_data = [{ 'id':result.id,
                          'code':result.work_code,
                          'permissible_work':result.permissible_work,
                          'parameter': result.name,
                          'input_value': result.input_value
                          } for result in results]
            json_data = sorted(json_data, key=lambda x: x['code'])

            grouped_data = defaultdict(list)
            for row in json_data:
                key = (row['code'], row['permissible_work'])                
                grouped_data[key].append({'id': row['id'], 'parameter': row['parameter'], 'input_value':row['input_value']})
            
            result = [{
                    'code': code,
                    'permissible_work':permissible_work, 
                    'field_data': fields
                    } for (code, permissible_work), fields in grouped_data.items()]

            return result
        else:
            return None
        
    # @classmethod
    # def get_asset_data_by_id(cls, asset_id):
    #     return None
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