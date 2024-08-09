from iWork.app.db import db

class InputParameter(db.Model):
    __tablename__ = "input_parameters"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(300))

    def __init__(self, name, description):
        self.name = name,
        self.description = description

    def json(self):
        return {
            'name': self.name,
            'description': self.description
        }
  