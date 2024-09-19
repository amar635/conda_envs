from iWork.app.db import db

class InputParameter(db.Model):
    __tablename__ = "input_parameters"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100)) # unique name of the input parameter
    label= db.Column(db.String(80)) # label for the input paramter
    unit = db.Column(db.String(80)) # unit of measurement 
    description = db.Column(db.String(300)) # details description of input parameter for (i) tooltip
    element_type = db.Column(db.String(100)) # whether dropdown, textbox or datalist
    constraint = db.Column(db.String(100))

    def __init__(self, name, label, unit, description, element_type, constraint):
        self.name = name,
        self.label = label,
        self.unit = unit,
        self.description = description
        self.element_type = element_type
        self.constraint = constraint

    def json(self):
        return {
            'name': self.name,
            'label' : self.label,
            'unit' : self.unit,
            'description': self.description,
            'element_type': self.element_type,
            'constraint': self.constraint
        }
  