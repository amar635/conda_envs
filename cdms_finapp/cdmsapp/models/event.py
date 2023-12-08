from cdmsapp.extensions import db

class EventModel(db.Model):
    __tablename__ = "events"

    event_id = db.Column(db.Integer, primary_key=True )
    event_title = db.Column(db.String(256), nullable=False)
    event_venue = db.Column(db.String(256), nullable=False)
    event_address = db.Column(db.String(256), nullable=False)
    event_date = db.Column(db.String(128), nullable=False)
    event_time = db.Column(db.String(128), nullable=False)

    participants = db.relationship("ParticipantModel", back_populates="event", lazy="dynamic")

    def json(self):
        return {
            'id': self.event_id,
            'event_title': self.event_title,
            'event_venue': self.event_venue,
            'event_address': self.event_address,
            'event_date': self.event_date,
            'event_time': self.event_time
        }

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(event_title=title).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(event_id=_id).first()
    
    @classmethod
    def get_all_events(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_to_db(self, event_data):
        event = self.find_by_id(event_data.event_id)
        event.event_address= event_data.event_address
        event.event_venue=event_data.event_venue
        event.event_date=event_data.event_date
        event.event_time=event_data.event_time
        event.event_title=event_data.event_title
        db.session.add(event)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()