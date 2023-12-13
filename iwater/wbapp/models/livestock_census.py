from wbapp.db_sqlalchemy import db

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
    def get_by_village_id(cls, village_id):
        return cls.query.filter_by(village_id=village_id).first()
        