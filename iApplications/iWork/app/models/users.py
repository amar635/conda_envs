from flask_login import UserMixin
from iWork.app.db import db

class User(UserMixin, db.Model):
    __tablename__ = 'tbl_users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self,name,username,password):
        self.password=password
        self.name=name
        self.username=username

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'password': self.password
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