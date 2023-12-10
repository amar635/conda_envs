from wbapp.db_sqlalchemy import db

class Waterbody(db.Model):
    __tablename__ = 'waterbodies'

    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('waterbodies_id_seq'::regclass)"))
    waterbody_area = db.Column(db.Float(53), nullable=False)
    village_id = db.Column(db.ForeignKey('villages.id'), nullable=False)

    village = db.relationship('Village')