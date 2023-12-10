from wbapp.db_sqlalchemy import db

class State(db.Model):
    __tablename__ = 'states'

    id = db.db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('states_id_seq'::regclass)"))
    name = db.Column(db.String(80))
    code = db.Column(db.Integer, nullable=False, unique=True)
    census_code = db.Column(db.Integer)