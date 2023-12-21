from sqlalchemy import case
from wbapp.db_sqlalchemy import db

class Waterbody(db.Model):
    __tablename__ = 'waterbodies'

    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('waterbodies_id_seq'::regclass)"))
    waterbody_area = db.Column(db.Float(53), nullable=False)
    village_id = db.Column(db.ForeignKey('villages.id'), nullable=False)

    village = db.relationship('Village')

    @classmethod
    def get_waterbodies(cls, village_ids):
        query = db.session.query(
        cls.waterbody_area,
            case(
                    (cls.waterbody_area < 10, 'small'),
                    (cls.waterbody_area > 100, 'large'),
                else_='medium'
            ).label('waterbody')
        ).filter(cls.village_id.in_(village_ids)).all()
        return query