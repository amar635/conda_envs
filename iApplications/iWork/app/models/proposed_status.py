from iWork.app.db import db
from iWork.app.models.categories import Category
from iWork.app.models.major_heads import MajorHead

class ProposedStatus(db.Model):
    __tablename__ = 'proposed_status_master'

    id = db.Column(db.Integer, primary_key= True)
    proposed_status=db.Column(db.String(80),nullable=False)
    work_type_id = db.Column(db.Integer,nullable = False) # to be deleted in the next version
    major_head_id = db.Column(db.ForeignKey('major_heads_master.id'), nullable=False)
    activity_type_id = db.Column(db.ForeignKey('activities_master.id'), nullable=False)
    beneficiary_type_id = db.Column(db.ForeignKey('beneficiaries_type_master.id'), nullable=False)
    master_work_type_id = db.Column(db.ForeignKey('work_types_master.id'), nullable=False)

    master_work_type = db.relationship('MasterWorkType')
    beneficiary_type = db.relationship('Beneficiary')
    acitivity_type = db.relationship('Activity')
    major_head = db.relationship('MajorHead')
    
    def __init__(self,proposed_status,work_type_id,beneficiary_type_id,activity_type_id,major_head_id,):
        self.proposed_status=proposed_status
        self.work_type_id = work_type_id
        self.beneficiary_type_id = beneficiary_type_id
        self.activity_type_id = activity_type_id
        self.major_head_id = major_head_id
    
    def json(self):
        return {
            'id': self.id,
            'proposed_status' : self.proposed_status,
            'work_type_id': self.work_type_id,
            'major_head_id' : self.major_head_id,
            'activity_type_id' : self.activity_type_id,
            'beneficiary_type_id' : self.beneficiary_type_id,
            'master_work_type_id': self.master_work_type_id
        }
        
    
    @classmethod
    def get_proposed_status_by_category(cls, category_id='All'):
        if category_id == "1" or category_id == "2" or category_id == "3" or category_id == "4":
            results = db.session.query(cls
            ).join(MajorHead, cls.major_head_id == MajorHead.id
            ).join(Category, Category.id == MajorHead.category_id
            ).filter(Category.id == category_id).all()
        else:
            results = cls.query.all()
        if results:
            permissible_works = []
            for result in results:
                permissible_works.append(result.json())
            return permissible_works
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
        query=cls.query.order_by(cls.name)
        return query

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(_id):
        proposed_status = ProposedStatus.query.filter_by(id=_id).first()
        db.session.delete(proposed_status)
        db.session.commit()

    def commit_db():
        db.session.commit()

    def update_db(data,_id):
        proposed_status = ProposedStatus.query.filter_by(id=_id).update(data)
        db.session.commit()