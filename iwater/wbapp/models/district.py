from wbapp.db_sqlalchemy import db

class District(db.Model):
    __tablename__ = 'districts'

    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('districts_id_seq'::regclass)"))
    name = db.Column(db.String(80), nullable=False)
    code = db.Column(db.Integer, nullable=False, unique=True)
    census_code = db.Column(db.Integer)
    state_id = db.Column(db.ForeignKey('states.id'), nullable=False)

    state = db.relationship('State')