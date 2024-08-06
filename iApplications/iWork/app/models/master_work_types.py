from iWork.app.db import db

class MasterWorkType(db.Model):
    ''' 
    These are the 39 work types under MGNREGA with effect from 01 April 2024
    '''
    __tablename__ = 'work_types_master'

    id = db.Column(db.Integer, primary_key= True)
    work_type=db.Column(db.String(200),nullable=False)
   
    def __init__(self,work_type):
        self.work_type=work_type
    
    def json(self):
        return {
            'id': self.id,
            'work_type' : self.work_type   
        }
    
    @classmethod
    def get_wb_by_id(cls, _id):
        query=cls.query.filter_by(id=_id).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_wb_by_type_id(cls, _type_id):
        query =  cls.query.filter_by(type_id=_type_id).first()
        if query:
            return query.json()
        else:
            return None
    
    @classmethod
    def get_all(cls):
        query=cls.query.order_by(cls.work_type)
        return query

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(_id):
        participant = MasterWorkType.query.filter_by(id=_id).first()
        db.session.delete(participant)
        db.session.commit()

    def commit_db():
        db.session.commit()

    def update_db(data,_id):
        user = MasterWorkType.query.filter_by(id=_id).update(data)
        db.session.commit()