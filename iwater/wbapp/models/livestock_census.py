from sqlalchemy import func
from wbapp.db_sqlalchemy import db
from wbapp.models.livestocks import Livestock

class LivestockCensus(db.Model):
    __tablename__ = 'livestock_census'
    __table_args__ = (
        db.UniqueConstraint('livestock_id', 'village_id'),
    )

    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('livestock_census_id_seq'::regclass)"))
    livestock_number = db.Column(db.Integer)
    livestock_id = db.Column(db.ForeignKey('livestocks.id'), nullable=False)
    village_id = db.Column(db.ForeignKey('villages.id'), nullable=False)

    livestock = db.relationship('Livestock')
    village = db.relationship('Village')

    @classmethod
    def get_by_village_id(cls, village_ids):
        query = db.session.query(
        Livestock.type,
        Livestock.name,
        func.sum(LivestockCensus.livestock_number).label('livestock_number'),
        func.avg(Livestock.water_use).label('water_use')
        ).join(Livestock, Livestock.id == LivestockCensus.livestock_id)\
        .filter(LivestockCensus.village_id.in_(village_ids))\
        .group_by(Livestock.id, Livestock.name, Livestock.type).all()
        return query
        