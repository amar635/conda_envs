from cdmsapp.extensions import db

class TokenBlocklistModel(db.Model):
    __tablename__ = "tokenblocklist"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)

    def json(self):
        return {
            'id': self.id,
            'jti': self.jti,
            'created_at': self.created_at
        }

    @classmethod
    def find_by_jti(cls, jti):
        return cls.query.filter_by(jti=jti).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # def delete_from_db(self):
    #     db.session.delete(self)
    #     db.session.commit()