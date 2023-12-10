from wbapp.db_sqlalchemy import db

class Block(db.Model):
    __tablename__ = 'blocks'

    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('blocks_id_seq'::regclass)"))
    name = db.Column(db.String(80))
    code = db.Column(db.Integer, nullable=False)
    census_code = db.Column(db.Integer)
    district_id = db.Column(db.ForeignKey('districts.id'), nullable=False)

    district = db.relationship('District')