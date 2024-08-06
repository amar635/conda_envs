from iWork.app.db import db

class District(db.Model):
    __tablename__ = 'nrega_districts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    nrega_id = db.Column(db.Integer, nullable=False, unique=True)
    state_id = db.Column(db.ForeignKey('nrega_states.id'), nullable=False)

    state = db.relationship('State')

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'nrega_id': self.nrega_id,
            'state_id': self.state_id
        }


    @classmethod
    def get_districts_by_state_id(cls, state_id):
        return cls.query.filter_by(state_id = state_id).order_by(cls.name).all()