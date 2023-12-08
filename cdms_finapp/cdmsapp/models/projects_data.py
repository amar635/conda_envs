from cdmsapp.extensions import db
from sqlalchemy import distinct, extract, func, and_, or_

class projectDataModel(db.Model):
    __tablename__ = "nrmae_projects"

    id = db.Column(db.Integer, primary_key=True)
    shortname = db.Column(db.String(128), nullable=False)
    fullname = db.Column(db.String(256), nullable=False)
    germanname = db.Column(db.String(256))
    project_type = db.Column(db.String(128))
    project_number = db.Column(db.String(128), nullable=False)
    implementing_partner = db.Column(db.String(128))
    implementing_states = db.Column(db.String(256))
    project_objective = db.Column(db.String(256))
    from_date = db.Column(db.String(64))
    to_date = db.Column(db.String(64))
    comm_value = db.Column(db.Float, nullable=False)
    av = db.Column(db.String(128))
    dv = db.Column(db.String(128))
    fm = db.Column(db.String(128))
    vgk = db.Column(db.Float)

    project_yearwise_financials = db.relationship("pywfModel", back_populates="project", lazy="dynamic")
    project_financials = db.relationship("FinancialDataModel", back_populates="project", lazy="dynamic")
    
    def json(self):
        return {
            'id': self.id,
            'shortName': self.shortname,
            'fullName': self.fullname,
            'germanName': self.germanname,
            'projectType': self.project_type,
            'projectNumber': self.project_number,
            'implementingPartner': self.implementing_partner,
            'implementingStates': self.implementing_states,
            'projectObjective': self.project_objective,
            'fromDate': self.from_date,
            'toDate': self.to_date,
            'commValue': self.comm_value,
            'av': self.av,
            'dv': self.dv,
            'fm': self.fm,
            'vgk': self.vgk
        }
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_shortname(cls, project_shortname):
        return cls.query.filter_by(shortname=project_shortname).first()

    @classmethod
    def find_by_pn(cls, project_number):
        return cls.query.filter_by(shortname=project_number).first()
    
    @classmethod
    def get_all_projects(cls):
        return cls.query.with_entities(cls.av,cls.dv,cls.comm_value, 
                cls.fm, cls.from_date, cls.fullname, cls.germanname, 
                cls.id, cls.shortname, cls.to_date, cls.vgk,
                cls.project_number,cls.project_type, cls.project_objective,
                cls.implementing_states, cls.implementing_partner, cls.id) \
                .order_by(cls.shortname)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

#     def update_to_db(self, cls):
#         participant = cls.query.filter_by(id=self.id)

#         if participant == None:
#             return None

#         participant.update({

#         })

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class pywfModel(db.Model):
    __tablename__ = "project_yearwise_financials"

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    tag = db.Column(db.String(10), nullable=False)
    budgeted = db.Column(db.Float)
    allocated = db.Column(db.Float)
    planned = db.Column(db.Float, nullable=False)

    projects_id = db.Column(db.Integer, db.ForeignKey("nrmae_projects.id"), unique=False, nullable=False)

    project = db.relationship("projectDataModel", back_populates="project_yearwise_financials")

    def json(self):
        return {
            'id': self.id,
            'year': self.year,
            'tag': self.tag,
            'budgeted': self.budgeted,
            'allocated': self.allocated,
            'planned': self.planned,
            'projects_id': self.projects_id
        }
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_projects_id(cls, _id):
        return cls.query.filter_by(projects_id=_id).order_by(cls.year).all()
    
    @classmethod
    def get_all_projects(cls):
        return cls.query.all()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    

