from flask_login import UserMixin
from iWork.app.db import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    state_id = db.Column(db.ForeignKey('nrega_states.id'), nullable=False)

    state = db.relationship('State')

    def __init__(self, name, username, password, state_id):
        self.password=password
        self.name=name
        self.username=username
        self.state_id = state_id

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'password': self.password,
            'state_id': self.state_id
        }


    # Class method to get a user by ID
    @classmethod
    def get_user_by_id(cls, _id):
        query = cls.query.filter_by(id=_id).first()
        if query:
            return query.json()
        else:
            return None
    
    # Class method to get a user by ID
    @classmethod
    def get_user_by_username(cls, username):
        query = cls.query.filter_by(username=username).first()
        if query:
            return query.json()
        else:
            return None
        
    @classmethod
    def update_db(cls,data,_id):
        user = cls.query.filter_by(id=_id).update(data)
        db.session.commit()
        return user
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()