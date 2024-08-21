from iWork.app.db import db

class InputParameter(db.Model):
    __tablename__ = "input_parameters"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100)) # unique name of the input parameter
    label= db.Column(db.String(80)) # label for the input paramter
    unit = db.Column(db.String(80)) # unit of measurement 
    description = db.Column(db.String(300)) # details description of input parameter for (i) tooltip

    def __init__(self, name, label, unit, description):
        self.name = name,
        self.label = label,
        self.unit = unit,
        self.description = description

    def json(self):
        return {
            'name': self.name,
            'label' : self.label,
            'unit' : self.unit,
            'description': self.description
        }
  