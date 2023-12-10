
from wbapp.db_sqlalchemy import db

class Village(db.Model):
    __tablename__ = 'villages'
    __table_args__ = (
        db.UniqueConstraint('block_id', 'district_id', 'code'),
    )

    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('villages_id_seq'::regclass)"))
    name = db.Column(db.String(160), nullable=False)
    code = db.Column(db.Integer, nullable=False)
    census_code = db.Column(db.Integer)
    block_id = db.Column(db.ForeignKey('blocks.id'), nullable=False)
    district_id = db.Column(db.ForeignKey('districts.id'), nullable=False)

    block = db.relationship('Block')
    district = db.relationship('District')